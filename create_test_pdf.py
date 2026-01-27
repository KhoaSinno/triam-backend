from fpdf import FPDF

# Tạo PDF với nội dung tiếng Việt có từ viết tắt
pdf = FPDF()
pdf.add_page()

# Add Unicode font for Vietnamese
pdf.add_font('DejaVu', '', 'C:/Windows/Fonts/arial.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)

content = """
Chào mừng các bạn sinh viên ngành CNTT!

Hôm nay chúng ta sẽ tìm hiểu về AI và cách các CEO 
ứng dụng nó trong DN của họ.

Theo thống kê, có khoảng 80% các DN tại Tp.HCM đã 
bắt đầu áp dụng Machine Learning vào quy trình NS.

Đặc biệt, phương pháp Agile đang rất phổ biến với 
tỷ lệ thành công lên đến 95%.

CNTT là ngành có tiềm năng phát triển rất lớn trong 
thời đại 4.0 hiện nay.
"""

pdf.multi_cell(0, 10, content)
pdf.output("test_book.pdf")
print("Đã tạo file test_book.pdf thành công!")
