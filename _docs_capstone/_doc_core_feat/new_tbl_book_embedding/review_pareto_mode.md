Mình đã đọc file `pareto_mode_gemini.json` và đối chiếu với EPUB `Of Mice and Men`. Đánh giá công tâm là:

**Pareto mode này chạy được, nội dung tóm tắt khá mượt, nhưng chưa nên coi là production-ready nếu bạn muốn đưa cho user học nghiêm túc. Nó phù hợp demo/beta hơn là production mặc định.**

## Kết quả đo nhanh

Với EPUB này, sách có 6 chapter, tổng khoảng **157k ký tự**. Pareto mode hiện tạo:

```text
total_sections = 6
total_units = 3
selected source_text_char_count = 58,900 / 157,166 ≈ 37.5%
generated segment text = 7,872 chars
generated audio duration ≈ 8 phút 57 giây
```

3 unit hiện tại là:

```text
Unit 1: Chapter 1 - setup George/Lennie/dream/safe haven
Unit 2: Chapter 5 - climax in the barn
Unit 3: Chapter 6 - tragic resolution
```

Tức là mode Pareto hiện chọn **chapter 1, 5, 6** và bỏ qua **chapter 2, 3, 4**.

## Điểm tốt

Về nội dung được chọn, các đoạn tóm tắt nhìn chung **đúng mạch truyện**, dễ nghe, tiếng Việt tự nhiên. Nó bắt được trục chính:

```text
George và Lennie
ước mơ về mảnh đất
tai họa ở chuồng ngựa
cái kết bên sông Salinas
```

Với người chỉ muốn nghe nhanh “cốt truyện chính xảy ra thế nào”, bản này dùng được.

Ngoài ra, segment audio khá ngắn, dễ phát trong app. Tổng audio khoảng 9 phút là hợp lý cho chế độ “học nhanh”.

## Vấn đề lớn nhất: bỏ chapter 2, 3, 4 hơi nặng

Nếu chỉ xét “main plot”, chọn chapter 1, 5, 6 là hiểu được đầu-cuối. Nhưng nếu xét “học tác phẩm”, bỏ chapter 2, 3, 4 sẽ mất rất nhiều thứ quan trọng:

```text
Chapter 2: ranch, boss, Curley, Slim, Curley's wife, hệ sinh thái trang trại.
Chapter 3: Candy, con chó của Candy, ước mơ trang trại được mở rộng, xung đột Curley-Lennie.
Chapter 4: Crooks, cô lập/chủng tộc, loneliness, sự mong manh của giấc mơ.
```

Đây không phải chi tiết phụ. Với `Of Mice and Men`, chapter 3 và 4 cực kỳ quan trọng về **theme**: cô đơn, quyền lực, phân biệt, giấc mơ Mỹ, người yếu thế.

Vì vậy nếu user học bằng Pareto mode này rồi hỏi:

```text
Candy quan trọng ở đâu?
Crooks đại diện cho điều gì?
Slim có vai trò gì?
Tại sao giấc mơ trang trại hấp dẫn nhiều người?
Curley's wife cô đơn như thế nào?
```

thì bản Pareto hiện tại cung cấp nền chưa đủ.

## Metadata có bug nghiêm trọng

Trường `estimated_audio_seconds` đang rất lệch so với audio thật.

Ví dụ:

```text
Unit 1 estimated_audio_seconds = 2077s ≈ 34 phút 37 giây
Unit 1 actual segment audio ≈ 139s ≈ 2 phút 19 giây

Unit 2 estimated_audio_seconds = 2042s ≈ 34 phút 02 giây
Unit 2 actual segment audio ≈ 106s ≈ 1 phút 46 giây

Unit 3 estimated_audio_seconds = 1042s ≈ 17 phút 22 giây
Unit 3 actual segment audio ≈ 292s ≈ 4 phút 52 giây
```

Nếu field này dùng cho UI, progress, schedule, estimated listening time, hoặc plan học thì **sai production**.

Cách sửa hợp lý:

```text
estimated_audio_seconds → đổi tên thành source_audio_estimate_seconds
thêm generated_audio_seconds = sum(segment.duration_ms) / 1000
```

Vì hiện tại có vẻ estimate đang tính theo source text gốc, không phải audio đã generate.

## Unit 3 bị mất cân bằng

Unit 1 có 6 segments, Unit 2 có 6 segments, Unit 3 có 16 segments.

Trong khi source chapter 6 ngắn hơn chapter 1 và 5, nhưng generated audio lại dài nhất:

```text
Unit 1: ~2m19s
Unit 2: ~1m46s
Unit 3: ~4m52s
```

Unit 3 chi tiết quá nhiều so với các unit trước. Không sai nội dung, nhưng UX học/nghe sẽ hơi lệch. Pareto mode nên có độ đều hơn, ví dụ mỗi unit 2–4 phút hoặc chia theo cùng kiểu narrative beat.

## Một số điểm ngôn ngữ cần chỉnh

Có vài chỗ dùng từ chưa tối ưu cho production:

```text
“cậu bé” để gọi Lennie
```

Lennie là người trưởng thành có hạn chế nhận thức, gọi “cậu bé” dễ làm sai sắc thái. Nên dùng:

```text
Lennie
anh
người đàn ông to lớn nhưng nhận thức hạn chế
```

Ngoài ra `planner_reason` đang lẫn tiếng Anh và tiếng Việt. Nếu field này chỉ internal thì không sao. Nếu có hiển thị cho user thì nên Việt hóa hoàn toàn.

## Rủi ro production về audio URL

Các `audio_url` đang là Supabase public URL. Với nội dung sinh ra từ EPUB, production nên cẩn thận:

```text
- Không để audio user upload thành public mặc định.
- Nên dùng private bucket hoặc signed URL.
- Audio chỉ nên truy cập bởi user sở hữu sách/session.
```

Nếu đây chỉ là dev/demo thì ổn. Nhưng production thật thì public audio URL là điểm cần khóa lại.

## Pareto mode hiện tại nên sửa theo hướng nào?

Với EPUB này, mình không khuyên chọn 1, 5, 6 riêng như hiện tại. Cấu trúc tốt hơn là 3 unit nhưng có unit gộp middle:

```text
Unit 1: Chapter 1
Setup George, Lennie, dream farm, safe place.

Unit 2: Chapter 2–4
Ranch society, Candy, Slim, Curley, Crooks, loneliness, dream under pressure.

Unit 3: Chapter 5–6
Accident, shattered dream, final decision, tragic resolution.
```

Hoặc nếu cho phép 4 unit thì tốt hơn nữa:

```text
Unit 1: Chapter 1 - Setup
Unit 2: Chapter 2–3 - Ranch conflict and Candy joins the dream
Unit 3: Chapter 4 - Crooks and loneliness
Unit 4: Chapter 5–6 - Tragedy and ending
```

Với sách này, bản 4 unit sẽ production hơn bản 3 unit hiện tại.

## Chấm điểm công tâm

```text
Nội dung từng đoạn: 8/10
Độ dễ nghe: 8/10
Độ đúng cốt truyện chính: 8/10
Độ đủ để học tác phẩm: 6/10
Cân bằng unit/segment: 6/10
Metadata production readiness: 5/10
Tổng thể production readiness: 6.5/10
```

## Kết luận

**Chưa nên lên production mặc định với EPUB này.**

Có thể dùng cho:

```text
demo
internal test
beta mode
quick recap mode
```

Nhưng nếu là production cho user học thật, mình khuyên chưa. Cần sửa tối thiểu:

```text
1. Sửa metadata duration: thêm generated_audio_seconds.
2. Không bỏ trống hoàn toàn chapter 2–4; nên tạo middle synthesis unit.
3. Cân bằng lại số segment/duration giữa các unit.
4. Sửa cách gọi Lennie, tránh “cậu bé”.
5. Nếu audio public, đổi sang private/signed URL.
6. Gắn nhãn rõ: “Tóm tắt nhanh/Pareto”, không phải “đầy đủ nội dung sách”.
```

Nói ngắn gọn: **ý tưởng Pareto mode ổn, chất lượng sinh nội dung khá tốt, nhưng planner chọn coverage chưa đủ thông minh cho sách này. Production được nếu là beta có disclaimer; chưa nên bật làm trải nghiệm chính.**
