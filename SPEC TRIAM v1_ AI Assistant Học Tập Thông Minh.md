# TEXT SPECIFICATION - TRIAM

## 1. Product Overview

- **Ten san pham:** TRIAM Assistant
- **Dinh vi:** AI Learning Companion cho nguoi ban ron, luoi doc, hoac muon hoc bang cach nghe va hoi dap chu dong.
- **Muc tieu:** Bien sach/tai lieu cua user thanh trai nghiem hoc tap bang audio, co ke hoach nghe, hoi dap realtime theo ngu canh, va on tap lap lai de ghi nho kien thuc.
- **Diem khac biet:** TRIAM khong chi la audiobook. TRIAM la doi tac hoc tap chu dong: doc giup, rut gon 80/20, lap ke hoach, nhac hoc, hoi dap, va goi lai kien thuc dung luc.

## 2. Target Users

- Sinh vien can hoc sach/tai lieu dai nhung thieu thoi gian.
- Nguoi muon nghe tai lieu khi di chuyen, lam viec nha, hoac truoc khi ngu.
- Nguoi can tro ly AI hoi dap trong pham vi sach/tai lieu da upload.
- Nguoi can duoc nhac nho de duy tri tien do va on tap.

## 3. Core Value Proposition

TRIAM giup user di qua 4 buoc:

```text
Upload tai lieu -> Tao ke hoach hoc -> Nghe/hoi dap -> Nhac hoc va on tap
```

Gia tri can chung minh trong capstone:

- Giam thoi gian tiep can sach/tai lieu.
- Giu ngu canh hoc tap theo tung sach/workspace.
- Cho phep nghe som khi audio dang duoc sinh tiep.
- Nhac user quay lai hoc va on tap kien thuc quan trong.

## 4. Main Business Workflows

### 4.1 Upload Document

User co the upload sach/tai lieu rieng hoac chon nguon tai lieu co san trong ung dung.

Backend can validate:

- Dinh dang: PDF, EPUB, DOCX.
- Dung luong file theo gioi han tai khoan.
- Cau truc tai lieu:
  - PDF can hidden outline/bookmarks.
  - EPUB can TOC/navigation.
  - DOCX can Heading/outline styles.
- Scanned/OCR/no outline: bao loi ro cho FE, khong fallback doan chuong bang regex.

Sau upload thanh cong:

- Tao `Book` status `draft`.
- Tao danh sach `Chapter` status `draft`.
- Tra outline ve FE de user xem truoc khi tao plan.

### 4.2 Create Reading Plan

User tao ke hoach hoc cho book da upload.

Input chinh:

- Book can hoc.
- Mode hoc: `full` hoac `pareto`.
- Pace/toc do hoc.
- Lich hoc mong muon.

Sau khi tao plan:

- Tao `ReadingPlan`.
- Tao `processing_jobs`.
- Book chuyen sang `processing`.
- Backend enqueue job xu ly ngam.
- FE co the poll progress de hien thi thanh tien do.

### 4.3 Listen Audio Early

Backend khong bat user doi het ca quyen sach moi nghe.

Business rule:

- Uu tien generate audio chapter dau tien.
- Khi co noi dung dau tien co the nghe, book co the chuyen `partial_ready`.
- FE unlock nut nghe khi co playable segments.
- Backend tiep tuc generate phan con lai.
- Khi xong het, book chuyen `ready`.

### 4.4 Study Modes

#### Full Mode

Full mode giu day du y chinh va thu tu noi dung goc, nhung bien thanh van noi tu nhien cho TTS.

Khong nen hieu full la doc nguyen van tung ky tu, vi PDF/DOCX/EPUB co nhieu loi format, header/footer, so trang.

#### Pareto Mode

Pareto mode la cach hoc 80/20:

- Giu lai dinh nghia, luan diem, quy trinh, cong thuc, keyword, ket luan quan trong.
- Luoc bo vi du dai, lap lai, noi dung phu.
- Tao script ngan gon nhung van lien ket va de nghe.

Trong dai han, Pareto nen co rubric/ranking kien thuc, khong chi doi system prompt.

### 4.5 Real-time Q&A

Trong luc nghe, user co the hoi AI khi khong hieu.

Business rule:

- Cau tra loi uu tien dua tren Study Context va tai lieu dang hoc.
- Neu can internet, can co co che bat/tat hoac xac nhan ro.
- Lich su chat gan voi Chat Thread.
- Voice va text transcript phai dong bo de FE ve bong bong chat on dinh.

### 4.6 Workspace / Study Context

User co the tao workspace/study context gom nhieu tai lieu.

Business rule:

- Mot Study Context co the gan nhieu Document/Book.
- Mot Study Context co the co nhieu Chat Thread.
- Direct Book Context dung cho luong chat nhanh theo tung book.
- Ve sau, tat ca phai gan voi `user_id` that tu auth, khong dung mock user trong production.

### 4.7 Reminders And Notifications

TRIAM can nhac user hoc tiep va on tap kien thuc.

Reminder types:

- **Plan reminder:** nhac user nghe theo lich.
- **Recovery reminder:** nhac khi user bo do/tre tien do.
- **Completion message:** dong vien khi user hoan thanh chapter/book.
- **Spaced review:** nhac lai kien thuc sau 1, 3, 7, 14, 30 ngay.

Business rule:

- Lich nhac phai ton trong timezone cua user.
- Co daily cap va quiet hours de tranh spam.
- Notification phai co idempotency key de tranh gui trung.
- Lich nhac nam trong DB, Celery Beat chi la bo quet dinh ky.

## 5. System States

Book status:

```text
draft -> processing -> partial_ready -> ready
                         |
                         -> error
```

Chapter status:

```text
draft -> processing -> ready
                   -> error
```

Processing job status:

```text
queued -> processing -> partial_ready -> ready
                         |
                         -> error/cancelled
```

## 6. Technical Direction

### Near Term

- DB progress + polling endpoint de FE hien thi progress bar.
- Them `processing_jobs`.
- Cap nhat worker hien tai de update progress.
- Validate token/size truoc LLM normalize.
- Unlock audio khi co first playable content.

### Mid Term

- Dua generate-plan va switch-mode sang Celery + Redis.
- Tach queues: document, llm, tts, embedding, notification.
- Them retry/idempotency.
- Them notification_outbox.

### Long Term

- Celery Beat scan due reminders/reviews.
- Spaced review dua tren review_text/knowledge atoms.
- Analytics ve completion rate va learning streak.
- Real auth user_id thay mock user.

## 7. Non-Functional Requirements

- **Cost control:** estimate token/audio minutes truoc khi xu ly nang.
- **Latency:** user duoc nghe som, khong doi full book.
- **Reliability:** job co retry va progress recover duoc sau restart.
- **Security:** khong log token, apikey, authorization header.
- **Clean architecture:** router mong, service xu ly business, repository chi DB, worker tu mo session.
- **Observability:** moi job co status, error message, current step.
