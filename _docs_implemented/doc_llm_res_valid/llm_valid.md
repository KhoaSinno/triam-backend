Anh đã check kỹ và fix luôn 3 lỗi gốc.

**Kết luận chính xác:**

1. Sách `a9453a82-6e22-42c7-bc4a-c8bd9125c422` upload DOCX thành công, parser ra đúng `18 chapters`.
2. Job `d8bac78e-5601-4779-bc3e-5263b71e561c` lỗi ở chương 2: `1.1 Giới thiệu`.
3. Chương 1 đã xử lý xong, có `5` audio segments.
4. Chương 2 lỗi vì LLM trả response không parse được JSON.
5. Chương 3 và 4 bị kẹt `processing` vì khi job fail, các task song song bị hủy nhưng chưa cleanup đúng.
6. Timeout upload FE 45s có nguyên nhân rõ: upload service đang commit DB từng chương. Với DOCX nhiều chương, riêng đoạn lưu DB có thể kéo dài rất lâu.

**Anh đã sửa:**

- [llm_service.py](W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/llm_service.py): đổi sang structured output có schema bằng `client.beta.chat.completions.parse(...)`, thêm validate và retry khi JSON lỗi.
- [upload_service.py](W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/upload_service.py): batch insert book + chapters trong một transaction, không commit từng chương nữa.
- [chapter_worker.py](W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/workers/chapter_worker.py): nếu một chapter fail làm hủy task khác, worker sẽ cleanup segments/knowledge/state, không để chapter kẹt `processing`.
- [book_pipeline.py](W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/app/services/workers/book_pipeline.py): cập nhật job progress khi fail rõ hơn.
- Update FE contract: [flutter_phase_4_backend_contract_uiux_guide.md](W:/WorkSpace_IT/_CAPSTON_PROJECT/triam-backend/_docs_implemented/doc_setup_flutter/flutter_phase_4_backend_contract_uiux_guide.md), thêm rule upload timeout nên là `120-180s`.

Anh cũng test đúng chương lỗi thật của sách này, không ghi DB: chương `1.1 Giới thiệu` đã normalize thành công với code mới.

**Test đã chạy:**

```text
ruff check: passed
py_compile: passed
pytest focused: 20 passed
real DOCX parser check: 18 chapters
real LLM isolated check chapter 2: passed
```

Nguồn kỹ thuật anh đối chiếu: Google khuyến nghị dùng structured output/schema và vẫn validate/error handling trong app: https://ai.google.dev/gemini-api/docs/structured-output

Lưu ý: book production hiện tại đã ở trạng thái `error`, nên sau khi deploy fix, cách test sạch nhất là xoá book đó rồi upload lại DOCX. Existing errored book chưa có retry endpoint riêng.
