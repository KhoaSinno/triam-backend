# THUẬT TOÁN: DFS INDEXING VÀ VALIDATION GATE

**Đầu vào (Data)**:
*   `Doc`: Tệp tài liệu thô (PDF/EPUB/DOCX)
*   `C`: Các ràng buộc kiểm duyệt (Validation Constraints)

**Đầu ra (Result)**:
*   `T_doc`: Cây cấu trúc tài liệu được phê duyệt
*   Hoặc báo lỗi `ParsingError`

### Giải thuật chi tiết (Mã giả)

```python
begin
    TextBlocks = ExtractTextAndStyle(Doc)
    RootNode = CreateNode("Document", Level = 0)
    ActivePath = [RootNode]
    
    foreach block b in TextBlocks:
        if IsHeader(b):
            H_level = GetHeaderLevel(b)
            NewNode = CreateNode(b.text, H_level)
            
            while Length(ActivePath) > 1 and Last(ActivePath).Level >= H_level:
                Pop(ActivePath)
            
            AddChild(Last(ActivePath), NewNode)
            Push(ActivePath, NewNode)
        else:
            AddParagraph(Last(ActivePath), b.text)
            
    # Cổng kiểm duyệt Validation Gate
    T_doc = RootNode
    V_passed = ValidateStructure(T_doc, C)
    
    if not V_passed:
        raise Error("Cấu trúc đề mục sách không hợp lệ hoặc quá lớn.")
        
    return T_doc
end
```

# BÀI CHẠY THỬ THUẬT TOÁN (DRY RUN)


Ta thiết lập một ví dụ giả lập là cuốn sách có nội dung gồm các khối văn bản (`TextBlocks`) sau:
1.  **Block 1**: `"Chương 1: Trí tuệ nhân tạo"` (Tiêu đề, Cấp độ 1)
2.  **Block 2**: `"Trí tuệ nhân tạo là..."` (Đoạn văn thường)
3.  **Block 3**: `"1.1 Học máy"` (Tiêu đề, Cấp độ 2)
4.  **Block 4**: `"Học máy tập trung vào..."` (Đoạn văn thường)
5.  **Block 5**: `"1.1.1 Học sâu"` (Tiêu đề, Cấp độ 3)
6.  **Block 6**: `"Học sâu sử dụng mạng nơ-ron..."` (Đoạn văn thường)
7.  **Block 6.5**: `"1.1.2 Học không giám sát"` (Tiêu đề, Cấp độ 3) — *Trường hợp anh em cùng cấp (siblings)*
8.  **Block 7**: `"1.2 Học tăng cường"` (Tiêu đề, Cấp độ 2) — *Trường hợp thụt lùi cấp độ ngược từ Level 3 về Level 2*
9.  **Block 8**: `"Học tăng cường là..."` (Đoạn văn thường)
10. **Block 9**: `"Chương 2: Khoa học dữ liệu"` (Tiêu đề, Cấp độ 1) — *Trường hợp thụt lùi mạnh từ Level 2 về Level 1*
11. **Block 10**: `"Khoa học dữ liệu là..."` (Đoạn văn thường)

Bộ ràng buộc kiểm duyệt $C$:
*   Tổng số đề mục tối đa: 300
*   Độ sâu tối đa: 6

---

## GIAI ĐOẠN 1: KHỞI TẠO (Dòng 1 - 4)

*   **Dòng 2 (`TextBlocks <- ExtractTextAndStyle(Doc)`)**:
    *   Hệ thống tải tệp sách và phân tách thành danh sách 10 blocks nêu trên.
*   **Dòng 3 (`RootNode <- CreateNode("Document", Level <- 0)`)**:
    *   Tạo nút cha lớn nhất của cả cuốn sách: `RootNode = { title: "Document", level: 0, children: [], paragraphs: [] }`.
*   **Dòng 4 (`ActivePath <- [RootNode]`)**:
    *   Stack `ActivePath` được khởi tạo: `ActivePath = [ RootNode ]` (kích thước Stack = 1).

---

## GIAI ĐOẠN 2: DUYỆT TỪNG KHỐI VĂN BẢN (Dòng 5 - 18)

### Vòng lặp 1: Xử lý Block 1 (`Chương 1: Trí tuệ nhân tạo`, Tiêu đề, Cấp độ 1)
*   **Dòng 5**: Duyệt block `b` = Block 1.
*   **Dòng 6 (`IsHeader(b)`)**: **Đúng** $\rightarrow$ Đi vào nhánh `if`.
*   **Dòng 7 (`H_level <- GetHeaderLevel(b)`)**: `H_level = 1`.
*   **Dòng 8 (`NewNode <- CreateNode(b.text, H_level)`)**:
    *   Tạo nút mới: `Node_Chương1 = { title: "Chương 1: Trí tuệ nhân tạo", level: 1, children: [], paragraphs: [] }`.
*   **Dòng 9-11 (`while Length(ActivePath) > 1 and Last(ActivePath).Level >= 1`)**:
    *   `Length(ActivePath) = 1` $\rightarrow$ Điều kiện `while` **Sai** (vòng lặp không chạy).
*   **Dòng 12 (`AddChild(Last(ActivePath), NewNode)`)**:
    *   Gắn `Node_Chương1` làm con của nút cuối Stack (hiện tại là `RootNode`).
    *   Cây hiện tại: `RootNode` $\rightarrow$ `Node_Chương1`.
*   **Dòng 13 (`Push(ActivePath, NewNode)`)**:
    *   Đẩy `Node_Chương1` vào Stack.
    *   Trạng thái Stack: `ActivePath = [ RootNode, Node_Chương1 ]`.

---

### Vòng lặp 2: Xử lý Block 2 (`Trí tuệ nhân tạo là...`, Đoạn văn thường)
*   **Dòng 5**: Duyệt block `b` = Block 2.
*   **Dòng 6 (`IsHeader(b)`)**: **Sai** $\rightarrow$ Nhảy sang nhánh `else` (Dòng 15).
*   **Dòng 16 (`AddParagraph(Last(ActivePath), b.text)`)**:
    *   Thêm đoạn văn này vào phần nội dung của nút cuối Stack (hiện tại là `Node_Chương1`).
    *   Cấu trúc dữ liệu: `Node_Chương1.paragraphs = ["Trí tuệ nhân tạo là..."]`.

---

### Vòng lặp 3: Xử lý Block 3 (`1.1 Học máy`, Tiêu đề, Cấp độ 2)
*   **Dòng 5**: Duyệt block `b` = Block 3.
*   **Dòng 6 (`IsHeader(b)`)**: **Đúng**.
*   **Dòng 7**: `H_level = 2`.
*   **Dòng 8**: Tạo nút `Node_Mục1.1` (`level = 2`).
*   **Dòng 9-11 (`while Length(ActivePath) > 1 and Last(ActivePath).Level >= 2`)**:
    *   `Length(ActivePath) = 2` (Đúng).
    *   `Last(ActivePath)` là `Node_Chương1` (`level = 1`). So sánh: `1 >= 2` $\rightarrow$ **Sai**.
    *   Vòng lặp `while` không chạy.
*   **Dòng 12**: Gắn `Node_Mục1.1` làm con của `Node_Chương1`.
*   **Dòng 13**: Đẩy `Node_Mục1.1` vào Stack.
    *   Trạng thái Stack: `ActivePath = [ RootNode, Node_Chương1, Node_Mục1.1 ]`.

---

### Vòng lặp 4: Xử lý Block 4 (`Học máy tập trung vào...`, Đoạn văn thường)
*   **Dòng 6 (`IsHeader(b)`)**: **Sai**.
*   **Dòng 16**: Gắn đoạn văn vào nút cuối Stack (`Node_Mục1.1`).
    *   Cấu trúc dữ liệu: `Node_Mục1.1.paragraphs = ["Học máy tập trung vào..."]`.

---

### Vòng lặp 5: Xử lý Block 5 (`1.1.1 Học sâu`, Tiêu đề, Cấp độ 3)
*   **Dòng 6 (`IsHeader(b)`)**: **Đúng**.
*   **Dòng 7**: `H_level = 3`.
*   **Dòng 8**: Tạo nút `Node_Mục1.1.1` (`level = 3`).
*   **Dòng 9-11 (`while ...`)**:
    *   `Last(ActivePath)` là `Node_Mục1.1` (`level = 2`). So sánh: `2 >= 3` $\rightarrow$ **Sai**.
    *   Vòng lặp không chạy.
*   **Dòng 12**: Gắn `Node_Mục1.1.1` làm con của `Node_Mục1.1`.
*   **Dòng 13**: Đẩy `Node_Mục1.1.1` vào Stack.
    *   Trạng thái Stack: `ActivePath = [ RootNode, Node_Chương1, Node_Mục1.1, Node_Mục1.1.1 ]`.

---

### Vòng lặp 6: Xử lý Block 6 (`Học sâu sử dụng mạng nơ-ron...`, Đoạn văn thường)
*   **Dòng 6**: **Sai**.
*   **Dòng 16**: Gắn đoạn văn vào nút cuối Stack (`Node_Mục1.1.1`).
    *   Cấu trúc dữ liệu: `Node_Mục1.1.1.paragraphs = ["Học sâu sử dụng mạng nơ-ron..."]`.

---

### Vòng lặp 6.5: Xử lý Block 6.5 (`1.1.2 Học không giám sát`, Tiêu đề, Cấp độ 3) — *Trường hợp anh em cùng cấp (siblings)*
*   **Dòng 6 (`IsHeader(b)`)**: **Đúng** $\rightarrow$ Đi vào nhánh `if`.
*   **Dòng 7 (`H_level <- GetHeaderLevel(b)`)**: `H_level = 3`.
*   **Dòng 8 (`NewNode <- CreateNode(b.text, H_level)`)**:
    *   Tạo nút mới: `Node_Mục1.1.2 = { title: "1.1.2 Học không giám sát", level: 3, children: [], paragraphs: [] }`.
*   **Dòng 9-11 (Vòng lặp `while` tìm cha)**:
    *   **Lần kiểm tra 1**:
        *   `Length(ActivePath) = 4 > 1` (Đúng).
        *   `Last(ActivePath)` là `Node_Mục1.1.1` (`level = 3`). So sánh: `3 >= 3` $\rightarrow$ **ĐÚNG** (Mục 1.1.2 không thể là con của Mục 1.1.1 vì chúng cùng cấp 3).
        *   **Dòng 10**: Thực hiện `Pop(ActivePath)` $\rightarrow$ Loại bỏ `Node_Mục1.1.1`.
        *   Stack lúc này còn: `ActivePath = [ RootNode, Node_Chương1, Node_Mục1.1 ]`.
    *   **Lần kiểm tra 2**:
        *   `Length(ActivePath) = 3 > 1` (Đúng).
        *   `Last(ActivePath)` hiện tại là `Node_Mục1.1` (`level = 2`). So sánh: `2 >= 3` $\rightarrow$ **SAI**.
        *   **Vòng lặp dừng lại!**
*   **Dòng 12 (`AddChild(Last(ActivePath), NewNode)`)**:
    *   Gắn `Node_Mục1.1.2` làm con của nút cuối Stack (hiện tại là `Node_Mục1.1`).
*   **Dòng 13 (`Push(ActivePath, NewNode)`)**:
    *   Đẩy `Node_Mục1.1.2` vào Stack.
    *   Trạng thái Stack: `ActivePath = [ RootNode, Node_Chương1, Node_Mục1.1, Node_Mục1.1.2 ]`.

---

### Vòng lặp 7: Xử lý Block 7 (`1.2 Học tăng cường`, Tiêu đề, Cấp độ 2) — *Trường hợp thụt lùi cấp độ ngược*
*   **Dòng 6**: **Đúng**.
*   **Dòng 7**: `H_level = 2`.
*   **Dòng 8**: Tạo nút `Node_Mục1.2` (`level = 2`).
*   **Dòng 9-11 (Vòng lặp `while`)**:
    *   **Lần kiểm tra 1**:
        *   `Length(ActivePath) = 4 > 1` (Đúng).
        *   `Last(ActivePath)` là `Node_Mục1.1.2` (`level = 3`). So sánh: `3 >= 2` $\rightarrow$ **ĐÚNG**.
        *   **Dòng 10**: Thực hiện `Pop(ActivePath)` $\rightarrow$ Loại bỏ `Node_Mục1.1.2`.
        *   Stack lúc này còn: `ActivePath = [ RootNode, Node_Chương1, Node_Mục1.1 ]`.
    *   **Lần kiểm tra 2**:
        *   `Length(ActivePath) = 3 > 1` (Đúng).
        *   `Last(ActivePath)` hiện tại là `Node_Mục1.1` (`level = 2`). So sánh: `2 >= 2` $\rightarrow$ **ĐÚNG** (Mục 1.2 không thể là con của Mục 1.1).
        *   **Dòng 10**: Thực hiện `Pop(ActivePath)` $\rightarrow$ Loại bỏ `Node_Mục1.1`.
        *   Stack lúc này còn: `ActivePath = [ RootNode, Node_Chương1 ]`.
    *   **Lần kiểm tra 3**:
        *   `Length(ActivePath) = 2 > 1` (Đúng).
        *   `Last(ActivePath)` hiện tại là `Node_Chương1` (`level = 1`). So sánh: `1 >= 2` $\rightarrow$ **SAI**.
        *   **Vòng lặp `while` dừng lại!**
*   **Dòng 12 (`AddChild(Last(ActivePath), NewNode)`)**:
    *   Gắn `Node_Mục1.2` làm con của `Node_Chương1` (vì `Node_Chương1` đang ở cuối Stack).
*   **Dòng 13**: Đẩy `Node_Mục1.2` vào Stack.
    *   Trạng thái Stack: `ActivePath = [ RootNode, Node_Chương1, Node_Mục1.2 ]`.

---

### Vòng lặp 8: Xử lý Block 8 (`Học tăng cường là...`, Đoạn văn thường)
*   **Dòng 6**: **Sai**.
*   **Dòng 16**: Gắn đoạn văn vào nút cuối Stack (`Node_Mục1.2`).
    *   Cấu trúc dữ liệu: `Node_Mục1.2.paragraphs = ["Học tăng cường là..."]`.

---

### Vòng lặp 9: Xử lý Block 9 (`Chương 2: Khoa học dữ liệu`, Tiêu đề, Cấp độ 1) — *Trường hợp thụt lùi cấp độ sâu*
*   **Dòng 6**: **Đúng**.
*   **Dòng 7**: `H_level = 1`.
*   **Dòng 8**: Tạo nút `Node_Chương2` (`level = 1`).
*   **Dòng 9-11 (Vòng lặp `while`)**:
    *   **Lần kiểm tra 1**:
        *   `Last(ActivePath)` là `Node_Mục1.2` (`level = 2`). So sánh: `2 >= 1` $\rightarrow$ **ĐÚNG**.
        *   **Dòng 10**: `Pop` loại bỏ `Node_Mục1.2`. Stack còn `[ RootNode, Node_Chương1 ]`.
    *   **Lần kiểm tra 2**:
        *   `Last(ActivePath)` hiện tại là `Node_Chương1` (`level = 1`). So sánh: `1 >= 1` $\rightarrow$ **ĐÚNG**.
        *   **Dòng 10**: `Pop` loại bỏ `Node_Chương1`. Stack còn `[ RootNode ]`.
    *   **Lần kiểm tra 3**:
        *   `Length(ActivePath) = 1` $\rightarrow$ **SAI** (không lớn hơn 1). Vòng lặp dừng lại!
*   **Dòng 12**: Gắn `Node_Chương2` làm con của `RootNode`.
*   **Dòng 13**: Đẩy `Node_Chương2` vào Stack.
    *   Trạng thái Stack: `ActivePath = [ RootNode, Node_Chương2 ]`.

---

### Vòng lặp 10: Xử lý Block 10 (`Khoa học dữ liệu là...`, Đoạn văn thường)
*   **Dòng 6**: **Sai**.
*   **Dòng 16**: Gắn đoạn văn vào nút cuối Stack (`Node_Chương2`).
    *   Cấu trúc dữ liệu: `Node_Chương2.paragraphs = ["Khoa học dữ liệu là..."]`.

---

## GIAI ĐOẠN 3: CỔNG KIỂM DUYỆT VALIDATION GATE (Dòng 19 - 25)

Sau khi duyệt hết các blocks, cấu trúc cây mục lục xây dựng được như sau:
```
RootNode (Level 0)
 ├── Chương 1: Trí tuệ nhân tạo (Level 1)
 │    ├── 1.1 Học máy (Level 2)
 │    │    ├── 1.1.1 Học sâu (Level 3)
 │    │    └── 1.1.2 Học không giám sát (Level 3)
 │    └── 1.2 Học tăng cường (Level 2)
 └── Chương 2: Khoa học dữ liệu (Level 1)
```

*   **Dòng 19 (`T_doc <- RootNode`)**: Gán toàn bộ cây trên vào `T_doc`.
*   **Dòng 20 (`V_passed <- ValidateStructure(T_doc, C)`)**:
    *   Hệ thống kiểm tra các chỉ số của cây `T_doc` đối chiếu với các ràng buộc $C$:
        *   *Tổng số đề mục*: 6 đề mục $\le$ 300 $\rightarrow$ **Hợp lệ**.
        *   *Độ sâu thư mục tối đa*: 3 cấp $\le$ 6 $\rightarrow$ **Hợp lệ**.
        *   *Trích xuất nội dung*: Có văn bản nguồn đầy đủ ở các chương $\rightarrow$ **Hợp lệ**.
    *   Kết quả trả về: `V_passed = True`.
*   **Dòng 21 (`if not V_passed`)**: Điều kiện **Sai** (không nhảy vào nhánh báo lỗi ở dòng 22).
*   **Dòng 24 (`return T_doc`)**: Trả về cấu trúc cây đã được kiểm duyệt thành công để chuyển sang bước tạo bài học Pareto và chunking.

---

### TRƯỜNG HỢP NGOẠI LỆ (FAIL CASE - Validation Gate từ chối)
Nếu cuốn sách được tải lên là một tệp scan hình ảnh không có mục lục, hoặc có cấu trúc bị lỗi phân cấp (ví dụ: mục lục lồng sâu đến 8 cấp, vượt giới hạn `max_depth = 6` của cấu hình $C$):
1.  Đến dòng 20: `ValidateStructure(T_doc, C)` quét qua cây và phát hiện độ sâu là 8.
2.  Kết quả trả về: `V_passed = False`.
3.  **Dòng 21 (`if not V_passed`)**: Điều kiện **Đúng**.
4.  **Dòng 22**: Kích hoạt `Raise Error("Cấu trúc đề mục sách không hợp lệ hoặc quá lớn.")`. 
5.  *Kết quả*: Hệ thống dừng xử lý ngay lập tức, hoàn tác (rollback) mọi giao dịch ghi tạm thời và trả về mã lỗi `422 Unprocessable Entity` cho phía Client.



# THUẬT TOÁN 2: GỘP XẾP HẠNG NGHỊCH ĐẢO RRF VÀ KIỂM TRA DANH SÁCH ỨNG VIÊN

**Đầu vào (Data)**:
*   `q`: Câu hỏi truy vấn của người dùng.
*   `C_v`: Danh sách các phân đoạn ứng viên thu được từ Vector Search.
*   `C_l`: Danh sách các phân đoạn ứng viên thu được từ Lexical Search.
*   `k = 60`: Hằng số làm mịn xếp hạng nghịch đảo.

**Đầu ra (Result)**:
*   `Selected`: Danh sách tối đa 6 phân đoạn ngữ cảnh được phê duyệt.
*   Hoặc từ chối (`Reject`) với mã lý do `"no_candidates"`.

### Giải thuật chi tiết (Mã giả)

```python
begin
    C_merged = MergeCandidates(C_v, C_l)
    Reranked = []
    
    # Xác định thứ tự xếp hạng (1-indexed) của ứng viên trong từng luồng
    Rank_vec = BuildRankMap(C_v)
    Rank_lex = BuildRankMap(C_l)
    
    foreach candidate c in C_merged:
        c_id = c.id
        term_v = 0.0
        term_l = 0.0
        
        if c_id in Rank_vec:
            term_v = 1.0 / (k + Rank_vec[c_id])
        if c_id in Rank_lex:
            term_l = 1.0 / (k + Rank_lex[c_id])
            
        c.final_score = term_v + term_l
        Add(Reranked, c)
        
    SortDescending(Reranked, key = final_score)
    Selected = SelectContext(Reranked, limit = 6)
    
    # Kiểm tra danh sách ứng viên
    if Length(Selected) == 0:
        return Reject("no_candidates")
        
    return Valid(Selected)
end
```

### Bài chạy thử (Dry Run)

Giả lập người dùng gửi truy vấn: `q = "Học sâu sử dụng mạng gì?"`
*   Kết quả Vector Search (`C_v`): `[Chunk_A (similarity = 0.85), Chunk_B (similarity = 0.70)]`
    *   Thứ hạng Vector: `Rank_vec = { "Chunk_A": 1, "Chunk_B": 2 }`
*   Kết quả Lexical Search (`C_l`): `[Chunk_B (lexical_score = 0.60), Chunk_C (lexical_score = 0.40)]`
    *   Thứ hạng Lexical: `Rank_lex = { "Chunk_B": 1, "Chunk_C": 2 }`
*   Danh sách gộp: `C_merged = [Chunk_A, Chunk_B, Chunk_C]`

**Tính toán điểm RRF từng phần tử ($k = 60$)**:
1.  **Chunk_A**:
    *   `term_v = 1.0 / (60 + 1) = 0.01639`
    *   `term_l = 0.0` (không xuất hiện ở lexical search)
    *   `final_score = 0.01639`
2.  **Chunk_B** (được cộng hưởng điểm từ cả hai nguồn search):
    *   `term_v = 1.0 / (60 + 2) = 0.01613`
    *   `term_l = 1.0 / (60 + 1) = 0.01639`
    *   `final_score = 0.01613 + 0.01639 = 0.03252`
3.  **Chunk_C**:
    *   `term_v = 0.0`
    *   `term_l = 1.0 / (60 + 2) = 0.01613`
    *   `final_score = 0.01613`

**Sắp xếp và Lọc ngữ cảnh**:
*   Sắp xếp giảm dần theo `final_score`: `[Chunk_B (0.03252), Chunk_A (0.01639), Chunk_C (0.01613)]`
*   Giới hạn lấy tối đa 6 đoạn: `Selected = [Chunk_B, Chunk_A, Chunk_C]`
*   Kiểm duyệt độ dài: `Length(Selected) = 3 > 0` $\rightarrow$ Điều kiện `Length(Selected) == 0` là **Sai**.
*   **Kết quả**: Trả về `Valid(Selected)` chứa 3 phân đoạn tri thức phù hợp.

---

# THUẬT TOÁN 3: SPACED REPETITION KẾT HỢP TRANSACTIONAL OUTBOX

**Đầu vào (Data)**:
*   `u`: Người dùng (User).
*   `LU`: Đơn vị bài học vừa được hoàn thành (Learning Unit).
*   `T_comp`: Thời điểm người học hoàn tất bài học.

**Đầu ra (Result)**:
*   Giao dịch (Transaction) được cam kết thành công trên DB bao gồm trạng thái bài học, chuỗi thẻ nhớ ôn tập ngắt quãng mới và tác vụ gửi thông báo tương ứng nằm trong hàng đợi Outbox.

### Giải thuật chi tiết (Mã giả)

```python
begin
    StartTransaction()
    try:
        SetStatus(LU, "Completed")
        CancelPendingUnanchoredReviews(u, LU)
        
        Intervals = [1, 3, 7, 14, 30]
        SequenceIndex = 0
        
        foreach d in Intervals:
            DueTime = T_comp + TimeDelta(d days)
            ReviewItem = CreateReviewItem(u, LU, DueTime, SequenceIndex)
            Save(ReviewItem)
            
            Key_idemp = Format("review:{0}:{1}:{2}", u.id, LU.id, d)
            OutboxRow = CreateOutboxRow(u.id, "spaced_review_due", DueTime, Key_idemp)
            Save(OutboxRow)
            
            SequenceIndex = SequenceIndex + 1
            
        CommitTransaction()
    except Exception as e:
        RollbackTransaction()
        return Error("Không thể lập lịch ôn tập ngắt quãng: " + e.message)
end
```

### Bài chạy thử (Dry Run)

Độc giả `u` (mã ID `u123`) học xong bài nghe `LU` (mã ID `lu456`) vào lúc `T_comp = 2026-07-06 08:00:00`.
1.  **Bắt đầu Giao dịch cơ sở dữ liệu** (`StartTransaction`).
2.  Cập nhật trạng thái học tập của `lu456` thành `"Completed"`.
3.  Quét tìm và hủy bỏ các thẻ ôn tập cùng đơn vị bài nghe cũ đang ở trạng thái chờ học mà chưa được ôn tập (`CancelPendingUnanchoredReviews`) để tránh lặp thẻ.
4.  Duyệt qua các ngày trong chu kỳ `Intervals = [1, 3, 7, 14, 30]`:
    *   **Ngày d = 1**:
        *   `DueTime = 2026-07-07 08:00:00`.
        *   Tạo và lưu thẻ ôn tập ngày 1 (`ReviewItem`).
        *   Tạo mã khóa chống lặp sự kiện: `Key_idemp = "review:u123:lu456:1"`.
        *   Ghi một bản ghi Outbox có trạng thái `PENDING`, hẹn thời điểm gửi là `2026-07-07 08:00:00`.
    *   **Ngày d = 3**:
        *   `DueTime = 2026-07-09 08:00:00`.
        *   Tạo và lưu thẻ ôn tập, kèm hàng outbox chống trùng `Key_idemp = "review:u123:lu456:3"`.
    *   *(Các chu kỳ 7, 14, 30 được lặp lại tương tự)*.
5.  **CommitTransaction**: Mọi bản ghi được lưu xuống đĩa cứng PostgreSQL đồng thời. Nếu có bất kỳ lỗi lưu trữ nào ở giữa chừng, toàn bộ các bản ghi tạo thẻ và outbox sẽ được **Rollback** sạch sẽ để tránh để lại dữ liệu rác.

---

# THUẬT TOÁN 4: PHÂN LOẠI Ý ĐỊNH CẤP QUYỀN TÌM KIẾM INTERNET THỜI GIAN THỰC

**Đầu vào (Data)**:
*   `Reply`: Câu trả lời thoại của người dùng khi được hỏi xin quyền tìm kiếm Internet.
*   `q_pending`: Truy vấn tìm kiếm Internet đang bị khóa chờ cấp quyền.
*   `State`: Máy trạng thái quản lý quyền sử dụng một lần (Permission State).

**Đầu ra (Result)**:
*   Quyết định phân loại ý định: `grant` (Đồng ý), `deny` (Từ chối), `unclear` (Không rõ), `new_question` (Hỏi câu mới).

### Giải thuật chi tiết (Mã giả)

```python
begin
    if State.status != "pending_permission":
        return "unclear"
        
    Reply_norm = LowerCase(Trim(Reply))
    
    # 1. Kiểm tra nhanh bằng bộ lọc Heuristics
    if MatchGrantPattern(Reply_norm):
        State.status = "granted"
        return "grant"
    if MatchDenyPattern(Reply_norm):
        State.status = "idle"
        return "deny"
        
    # 2. Phân loại sâu bằng LLM Classifier khi bộ lọc Heuristics không đối khớp
    try:
        (Decision, Confidence) = ClassifyWithTimeout(q_pending, Reply, timeout = 5.0)
        
        if Confidence < 0.72:
            return "unclear"
            
        if Decision in ["deny", "new_question"]:
            State.status = "idle"
        if Decision == "grant":
            State.status = "granted"
            
        return Decision
    except Exception:
        return "unclear"
end
```

### Bài chạy thử (Dry Run)

*   **Trường hợp A (Khớp Heuristic - Đồng ý nhanh)**:
    *   Hệ thống hỏi xin quyền, đưa máy trạng thái về `pending_permission`. Người dùng trả lời: `"Đồng ý đi"`.
    *   Chuẩn hóa: `Reply_norm = "đồng ý đi"`.
    *   `MatchGrantPattern` phát hiện chứa từ khóa đồng ý $\rightarrow$ Trả về `True`.
    *   Cập nhật `State.status = "granted"`.
    *   *Kết quả*: Trả về `grant` ngay lập tức mà không tốn tài nguyên và thời gian gọi LLM.
*   **Trường hợp B (Gọi LLM phân loại sâu - Đồng ý ngầm định)**:
    *   Người dùng trả lời phức tạp: `"Ừ tìm giúp tôi đi xem trên mạng có thông tin gì mới không"`.
    *   Bộ lọc heuristics từ chối đối khớp. Hệ thống chuyển sang gọi API LLM (`gpt-4o-mini`) phân loại.
    *   LLM trả về: `Decision = "grant"`, `Confidence = 0.96`.
    *   So sánh độ tin cậy: `0.96 >= 0.72` $\rightarrow$ Hợp lệ.
    *   Cập nhật máy trạng thái `State.status = "granted"`.
    *   *Kết quả*: Trả về `grant`.
*   **Trường hợp C (Không rõ ý định)**:
    *   Người dùng trả lời lấp lửng hoặc đổi chủ đề: `"Tôi cũng chưa biết, à mà thời tiết hôm nay thế nào nhỉ?"`.
    *   Heuristics không khớp. Gọi LLM trả về độ tin cậy thấp: `Confidence = 0.45` (hoặc trả về phân loại không rõ ràng).
    *   So sánh độ tin cậy: `0.45 < 0.72` $\rightarrow$ Điều kiện dừng hoạt động.
    *   *Kết quả*: Trả về `unclear`, Agent đàm thoại sẽ nhắc lại câu hỏi xin quyền và không tự ý truy cập Internet.
