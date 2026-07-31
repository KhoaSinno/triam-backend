---
name: triam-thesis-latex
description: Rules, workflow, image conversion, and compilation instructions for the TRIAM LaTeX thesis repo at D:\2022DoAnTN_KhoaDat or thesis LaTeX source code. Use when editing luanvan.tex, luanvan.sty, noidung/, hinhve/, sodo/, tools/, or compiling LaTeX documents for the TRIAM capstone thesis.
---

# Triam Thesis LaTeX Workflow & Guidelines

Skill này dùng cho repo luận văn Tri Âm tại `D:\2022DoAnTN_KhoaDat` (hoặc các file nguồn LaTeX luận văn).

## 1. Cấu Trúc File & Quy Ước Nhánh
- **File build chính:** `luanvan.tex`
- **File định dạng / package chung:** `luanvan.sty` và `luanvan_pack.sty`. *(Khi sửa phải cẩn thận vì ảnh hưởng rộng toàn bộ tài liệu).*
- **Nội dung các chương:** Nằm trong thư mục `noidung/`.
- **Hình vẽ:** Nằm trong thư mục `hinhve/`.
- **Sơ đồ:** Nằm trong thư mục `sodo/`.
- **Script tiện ích:** Nằm trong thư mục `tools/`.
- **Văn phong & Ngôn ngữ:** Khi chỉnh sửa luận văn, phải giữ nguyên văn phong, tiêu đề, chú thích (captions), nhãn (labels) và tên giao diện UI bằng tiếng Việt theo quy ước hiện có.

## 2. Quy Tắc Làm Việc (Workflow Rules)
1. **Kiểm tra trạng thái Git:** Luôn kiểm tra `git status --short --branch` trước khi thực hiện bất kỳ sửa đổi nào.
2. **Bảo tồn thay đổi hiện có:** Repo thường có sẵn các thay đổi dở dang, tuyệt đối không được revert hoặc stage các thay đổi không liên quan.
3. **Quy trình Commit:** Nếu được yêu cầu commit, phải kiểm tra kỹ phạm vi thay đổi, thông báo commit hash, kết quả push và trạng thái dirty còn lại.
4. **Phạm vi sửa đổi:** Ưu tiên sửa hẹp đúng file cần thiết, tránh rewrite/reformat rộng trong `.sty` nếu không được yêu cầu.

## 3. Workflow Biên Dịch LaTeX
- **Lệnh biên dịch tiêu chuẩn:**
  ```bash
  latexmk -pdf -interaction=nonstopmode -file-line-error luanvan.tex
  ```
- **Kiểm tra Môi trường:** Nếu `latexmk` hoặc `pdflatex` không có trong `PATH`, cần kiểm tra cài đặt TeX Live / MiKTeX và các biến môi trường trước khi kết luận thiếu LaTeX.

## 4. Workflow Xử Lý Hình Ảnh UI (Chương 9)
- **Vị trí ảnh:** Đặt ảnh chụp màn hình vào `hinhve/c9_xay_dung_he_thong/`.
- **Đặt tên theme Light/Dark:** Nếu có cặp ảnh sáng/tối, giữ nguyên quy chuẩn đặt tên: `ui_xxx_light.png` và `ui_xxx_dark.png`.
- **Kết hợp theme:** Chỉ combine các cặp ảnh light/dark đã được duyệt bằng script:
  ```bash
  python tools/combine_theme_screenshots.py
  ```
- **Chuyển đổi Định dạng Ảnh:** Chuyển đổi các file ảnh raster sang PDF bằng script:
  ```bash
  python tools/image_to_pdf.py
  ```
- **Import vào LaTeX:** Trong file LaTeX, chỉ import trực tiếp file `.pdf`, **KHÔNG import trực tiếp file `.png`**.
- **File giao diện ổn định:** File tập trung cho chương giao diện là `noidung/c9_xay_dung_he_thong/c9_05_giao_dien.tex`.

## 5. Kiểm Tra Sau Khi Sửa Đổi
- **Sau khi sửa đổi lớn:**
  ```bash
  git diff --check
  latexmk -pdf -interaction=nonstopmode -file-line-error luanvan.tex
  ```
- **Chú ý:** Nếu chỉ sửa text nhỏ và chưa chạy build đầy đủ, phải báo rõ cho người dùng biết là chưa chạy build.
