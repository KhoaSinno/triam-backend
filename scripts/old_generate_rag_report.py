import time

from openai import OpenAI
from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.models.db_models import Book, BookKnowledge

QUESTIONS = [
    "Nội dung chính của sách này là gì?",
    "Ai là nhân vật chính của quyển sách?",
    "Một số câu nói hay hoặc châm ngôn trong sách?",
    "Bài học lớn nhất rút ra từ cuốn sách này là gì?",
    "Có sự kiện lớn nào mở đầu câu chuyện không?",
    "Hoàn cảnh sáng tác hoặc bối cảnh của sách?",
    "Ai là tác giả của quyển sách?",
    "Cách để áp dụng kiến thức trong sách vào thực tế?",
    "Phần kết của sách như thế nào?",
    "Cuốn sách này phù hợp cho đối tượng người đọc nào?",
]


def generate_rag_report():
    engine = create_engine(settings.DATABASE_URL)
    report_lines = ["# Báo cáo Kiểm thử Thực tế API RAG Vector Search\n"]
    report_lines.append("> [!NOTE]")
    report_lines.append("> Đây là kết quả kiểm thử tự động truy vấn 10 câu hỏi đối với hệ thống Cơ sở dữ liệu Supabase Vector (pgvector).")
    report_lines.append("> Hệ thống sẽ dùng OpenAI `text-embedding-3-small` để nhúng câu hỏi, và dùng hàm RPC `match_book_knowledge` để tìm 3 đoạn văn có mức độ tương đồng cao nhất.\n")

    with Session(engine) as session:
        bk = session.exec(select(BookKnowledge).limit(1)).first()
        if not bk:
            report_lines.append("❌ Lỗi: Không tìm thấy sách nào chứa dữ liệu Knowledge (Vector) trong Database.")
            with open("C:/Users/Lenovo/.gemini/antigravity/brain/c2c55760-2fb5-462d-8749-b8e186c19224/rag_test_report.md", "w", encoding="utf-8") as f:
                f.write("\n".join(report_lines))
            return

        book_id = bk.book_id
        book = session.get(Book, book_id)
        b_title = book.title if book else "Unknown"

        report_lines.append(f"**📚 Sách đang test:** `{b_title}` (ID: `{book_id}`)\n")
        report_lines.append("---\n")

        from app.core.supabase import supabase

        ai = OpenAI(api_key=settings.OPENAI_API_KEY)

        for idx, q in enumerate(QUESTIONS, 1):
            report_lines.append(f"## Câu hỏi {idx}: {q}")
            try:
                # Embedding
                t1 = time.time()
                res = ai.embeddings.create(model="text-embedding-3-small", input=[q])
                query_vector = res.data[0].embedding

                # RPC RAG
                result = supabase.rpc(
                    "match_book_knowledge",
                    {
                        "query_embedding": query_vector,
                        "match_threshold": 0.1,  # Cho phép lấy cả kết quả similarity thấp để xem data
                        "match_count": 3,
                        "filter_book_id": str(book_id),
                    },
                ).execute()
                t2 = time.time()

                duration = round((t2 - t1) * 1000, 2)
                report_lines.append(f"*Thời gian xử lý (Embed + Supabase):* `{duration} ms`")
                report_lines.append(f"*Số đoạn tìm thấy:* `{len(result.data)}`\n")

                if result.data:
                    for count, row in enumerate(result.data, 1):
                        similarity = round(row.get("similarity", 0), 4)
                        report_lines.append(f"#### Kết quả {count} (Độ khớp: {similarity * 100}%)")
                        report_lines.append(f"```text")
                        content = row.get("content", "")
                        # Thu gọn nếu quá dài
                        if len(content) > 500:
                            content = content[:500] + " ... [LƯỢC BỚT]"
                        report_lines.append(content)
                        report_lines.append(f"```\n")
                else:
                    report_lines.append("> [!WARNING]")
                    report_lines.append("> Hệ thống không tìm thấy nội dung nào liên quan trong sách khớp với câu hỏi này.\n")

            except Exception as e:
                report_lines.append("> [!CAUTION]")
                report_lines.append(f"> Lỗi phát sinh: {e}\n")

            report_lines.append("---\n")

    # Ghi thành file trong workspace
    import os

    os.makedirs("_log_extracted_json", exist_ok=True)
    output_path = "_log_extracted_json/rag_test_report.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"Report generated successfully at: {output_path}")


generate_rag_report()
