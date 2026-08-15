"""
scripts/purge_orphan_storage_assets.py
========================================
Tool để rà soát (audit) và dọn dẹp (purge) các file audio và file sách rác
trên Supabase Storage không còn liên kết với bất kỳ bản ghi DB hợp lệ nào.

Sử dụng:
    # 1. Chỉ rà soát (Audit mode - không xóa):
    uv run python scripts/purge_orphan_storage_assets.py --dry-run

    # 2. Xóa sạch file rác (Purge mode):
    uv run python scripts/purge_orphan_storage_assets.py
"""

import argparse
from sqlmodel import Session, select

from app.db.database import engine
from app.models.db_models import Book, LearningUnit, LearningUnitSegment
from app.core.supabase import supabase
from app.core.logger import log as logger


def get_all_storage_folders(bucket_name: str) -> list[str]:
    folders = []
    limit = 100
    offset = 0
    while True:
        res = supabase.storage.from_(bucket_name).list(options={"limit": limit, "offset": offset})
        if not res:
            break
        names = [item["name"] for item in res if isinstance(item, dict) and item.get("name")]
        folders.extend(names)
        if len(res) < limit:
            break
        offset += limit
    return folders


def audit_and_purge_storage(*, dry_run: bool = False) -> None:
    logger.info(f"Bắt đầu audit Supabase Storage | dry_run={dry_run}")
    
    with Session(engine) as session:
        db_books = session.exec(select(Book)).all()
        db_book_ids = set(str(b.id) for b in db_books)
        
        segments = session.exec(select(LearningUnitSegment.audio_url)).all()
        units = session.exec(select(LearningUnit.review_audio_url)).all()
        valid_urls = set(s for s in segments if s) | set(u for u in units if u)

    print(f"[*] Tổng số sách hoạt động trong DB: {len(db_book_ids)}")
    print(f"[*] Tổng số URL audio hợp lệ trong DB: {len(valid_urls)}")

    # 1. Bucket 'audios'
    audio_folders = get_all_storage_folders("audios")
    print(f"[*] Tổng thư mục top-level trong bucket 'audios': {len(audio_folders)}")
    
    orphan_audio_files = []
    for folder in audio_folders:
        res = supabase.rpc("get_book_asset_paths", {"bucket_names": ["audios"], "book_id_prefix": folder}).execute()
        if res.data:
            paths = [item["name"] for item in res.data if isinstance(item, dict)]
            if folder not in db_book_ids:
                orphan_audio_files.extend(paths)
            else:
                for p in paths:
                    if not any(p in u for u in valid_urls):
                        orphan_audio_files.append(p)
        else:
            if folder not in db_book_ids:
                files = supabase.storage.from_("audios").list(folder)
                for f in files:
                    if isinstance(f, dict) and f.get("name"):
                        orphan_audio_files.append(f"{folder}/{f['name']}")

    # 2. Bucket 'raw_books'
    raw_folders = get_all_storage_folders("raw_books")
    print(f"[*] Tổng mục top-level trong bucket 'raw_books': {len(raw_folders)}")
    
    orphan_raw_files = []
    for item in raw_folders:
        prefix = item.split('/')[0]
        if prefix not in db_book_ids:
            res = supabase.rpc("get_book_asset_paths", {"bucket_names": ["raw_books"], "book_id_prefix": prefix}).execute()
            if res.data:
                paths = [i["name"] for i in res.data if isinstance(i, dict)]
                orphan_raw_files.extend(paths)
            else:
                orphan_raw_files.append(item)

    orphan_raw_files = list(set(orphan_raw_files))

    print("\n" + "="*50)
    print(f"BÁO CÁO AUDIT FILE RÁC (STORAGE ORPHANS):")
    print(f"  - File audio rác trong 'audios': {len(orphan_audio_files)} files")
    print(f"  - File sách gốc rác trong 'raw_books': {len(orphan_raw_files)} files")
    print(f"  - TỔNG FILE RÁC: {len(orphan_audio_files) + len(orphan_raw_files)} files")
    print("="*50 + "\n")

    if dry_run:
        print("[DRY-RUN] Không thực hiện xóa. Hãy chạy không có cờ --dry-run để xóa sạch.")
        return

    if not orphan_audio_files and not orphan_raw_files:
        print("[SUCCESS] Storage đã hoàn toàn sạch sẽ, không có file rác nào để xóa.")
        return

    # Thực hiện xóa batch 100 files
    batch_size = 100
    deleted_audios = 0
    for i in range(0, len(orphan_audio_files), batch_size):
        batch = orphan_audio_files[i:i + batch_size]
        try:
            supabase.storage.from_("audios").remove(batch)
            deleted_audios += len(batch)
            print(f"--> Đã xóa batch audio {i//batch_size + 1}: {len(batch)} files")
        except Exception as e:
            logger.error(f"Lỗi khi xóa batch audios: {e}")

    deleted_raw = 0
    for i in range(0, len(orphan_raw_files), batch_size):
        batch = orphan_raw_files[i:i + batch_size]
        try:
            supabase.storage.from_("raw_books").remove(batch)
            deleted_raw += len(batch)
            print(f"--> Đã xóa batch raw_books {i//batch_size + 1}: {len(batch)} files")
        except Exception as e:
            logger.error(f"Lỗi khi xóa batch raw_books: {e}")

    # Xóa folder rác rỗng nếu có
    orphan_empty_folders = [f for f in audio_folders if f not in db_book_ids]
    for folder in orphan_empty_folders:
        try:
            supabase.storage.from_("audios").remove([f"{folder}/.emptyFolderPlaceholder", f"{folder}/"])
        except Exception:
            pass

    print(f"\n[HOÀN TẤT] Đã dọn dẹp thành công {deleted_audios} file audio và {deleted_raw} file raw_books!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit and purge orphan storage assets from Supabase Storage.")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ kiểm tra và báo cáo, không xóa file.")
    args = parser.parse_args()
    
    audit_and_purge_storage(dry_run=args.dry_run)
