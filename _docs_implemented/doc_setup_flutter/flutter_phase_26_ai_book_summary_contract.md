# Phase 26 Frontend API Contract & UI/UX Integration Guide: AI Book Summary

Tài liệu này là hợp đồng tích hợp chính thức (API Contract) dành riêng cho các lập trình viên **Flutter Frontend** để hiện thực tính năng **AI Tóm Tắt Sách (`showBookDetailAiSummarySheet`)** từ giao diện `C:\triam-frontend\lib\shared\book\presentation\book_detail\book_detail_sheet_launchers.dart`.

---

## 1. Danh Sách API Endpoints (Backend Specs)

### 1.1. Lấy bản tóm tắt AI của sách (Cache-first < 20ms)
* **HTTP Method:** `GET`
* **Path:** `/api/v1/books/{book_id}/summary`
* **Headers:** `Authorization: Bearer <user_access_token>`

#### Response Body (Status 200 OK):
```json
{
  "book_id": "e447b894-4646-46db-a33b-2a073a14723b",
  "status": "completed",
  "ai_summary": {
    "key_idea": "Cuốn sách kể về cuộc phiêu lưu kịch tính của nhà Arnold và Hoàng tử Paul tại Lâu đài Moon...",
    "target_audience": "Độc giả yêu thích thể loại trinh thám, phiêu lưu kỳ bí (12+).",
    "estimated_read_minutes": 240,
    "key_takeaways": [
      "Lòng dũng cảm giúp vượt qua sợ hãi.",
      "Tình bạn và sự hợp tác là chìa khóa giải quyết thử thách."
    ],
    "summary": "Câu chuyện bắt đầu khi Nora và Peggy chờ đợi anh em song sinh Mike...",
    "main_characters": [
      "Jack",
      "Mike Arnold",
      "Prince Paul"
    ]
  },
  "error_message": null
}
```

#### Các giá trị trạng thái `status`:
| Trạng thái `status` | Ý nghĩa nghiệp vụ | Hành vi phía Flutter FE |
|---|---|---|
| `"pending"` / `"processing"` | Worker đang chạy ngầm sinh tóm tắt bên Backend | Hiển thị hiệu ứng chờ Skeleton Loader |
| `"completed"` | Đã tạo xong bản tóm tắt | Hiển thị dữ liệu 4 Card chi tiết |
| `"failed"` | Tạo thất bại sau 3 lần retry | Hiển thị thẻ báo lỗi + Nút **"Thử lại"** |

---

### 1.2. Yêu cầu tạo lại bản tóm tắt AI dưới nền (Regenerate)
* **HTTP Method:** `POST`
* **Path:** `/api/v1/books/{book_id}/summary/regenerate`
* **Headers:** `Authorization: Bearer <user_access_token>`

#### Response Body (Status 200 OK):
```json
{
  "message": "Đã gửi yêu cầu tạo lại tóm tắt AI dưới nền.",
  "status": "pending"
}
```

> [!IMPORTANT]
> **CAM KẾT HIỆU NĂNG & TRẢI NGHIỆM NGƯỜI DÙNG (NON-BLOCKING & ZERO UI FREEZE):**
> 1. Lệnh `POST /regenerate` phản hồi tức thì trong **< 20ms** vì chỉ chuyển trạng thái DB thành `"pending"` và gửi Celery Background Task.
> 2. **Hoàn toàn KHÔNG gây đơ / giật lag UI Flutter.**
> 3. Sau khi bấm nút "Thử lại", FE chuyển UI sang trạng thái Skeleton Loading và thực hiện Polling nhẹ (cứ 5 giây gọi `GET /summary` 1 lần cho đến khi `status == "completed"`).

---

## 2. Bảng Máp Dữ Liệu 1-to-1 Với Giao Diện Flutter UI

Máp trực tiếp các trường dữ liệu từ `ai_summary` vào Widget `showBookDetailAiSummarySheet` trong file `book_detail_sheet_launchers.dart`:

```dart
// 1. Ý tưởng chính (Icon: Icons.lightbulb_outline)
BookDetailAiSummaryItem(
  icon: Icons.lightbulb_outline,
  title: 'Ý tưởng chính',
  content: summaryData.aiSummary?.keyIdea ?? 'Chưa có thông tin',
),

// 2. Đối tượng phù hợp (Icon: Icons.group_outlined)
BookDetailAiSummaryItem(
  icon: Icons.group_outlined,
  title: 'Đối tượng phù hợp',
  content: summaryData.aiSummary?.targetAudience ?? 'Chưa có thông tin',
),

// 3. Thời gian đọc ước tính (Icon: Icons.timer_outlined)
BookDetailAiSummaryItem(
  icon: Icons.timer_outlined,
  title: 'Thời gian đọc ước tính',
  content: summaryData.aiSummary?.estimatedReadMinutes != null
      ? 'Khoảng ${(summaryData.aiSummary!.estimatedReadMinutes / 60).toStringAsFixed(1)} giờ (${summaryData.aiSummary!.estimatedReadMinutes} phút)'
      : 'Chưa có thông tin',
),

// 4. Đánh giá tổng quan / Key Takeaways (Icon: Icons.star_outline)
BookDetailAiSummaryItem(
  icon: Icons.star_outline,
  title: 'Đánh giá tổng quan',
  content: summaryData.aiSummary?.keyTakeaways.isNotEmpty == true
      ? summaryData.aiSummary!.keyTakeaways.map((e) => '• $e').join('\n')
      : 'Chưa có thông tin',
),
```

---

## 3. Mã Nguồn Mẫu Dart / Flutter Data Model & Provider

### 3.1. Dart Model (`book_ai_summary_model.dart`)

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'book_ai_summary_model.freezed.dart';
part 'book_ai_summary_model.g.dart';

@freezed
class BookAiSummaryContent with _$BookAiSummaryContent {
  const factory BookAiSummaryContent({
    @JsonKey(name: 'key_idea') required String keyIdea,
    @JsonKey(name: 'target_audience') required String targetAudience,
    @JsonKey(name: 'estimated_read_minutes') required int estimatedReadMinutes,
    @JsonKey(name: 'key_takeaways') @Default([]) List<String> keyTakeaways,
    required String summary,
    @JsonKey(name: 'main_characters') @Default([]) List<String> mainCharacters,
  }) = _BookAiSummaryContent;

  factory BookAiSummaryContent.fromJson(Map<String, dynamic> json) =>
      _$BookAiSummaryContentFromJson(json);
}

@freezed
class BookAiSummaryResponse with _$BookAiSummaryResponse {
  const factory BookAiSummaryResponse({
    @JsonKey(name: 'book_id') required String bookId,
    required String status,
    @JsonKey(name: 'ai_summary') BookAiSummaryContent? aiSummary,
    @JsonKey(name: 'error_message') String? errorMessage,
  }) = _BookAiSummaryResponse;

  factory BookAiSummaryResponse.fromJson(Map<String, dynamic> json) =>
      _$BookAiSummaryResponseFromJson(json);
}
```

---

### 3.2. Xử Lý Trạng Thái UI Trong `showBookDetailAiSummarySheet`

```dart
void showBookDetailAiSummarySheet({
  required BuildContext context,
  required Book book,
  required bool isUserBook,
  required int savedCount,
}) {
  showModalBottomSheet<void>(
    context: context,
    isScrollControlled: true,
    builder: (context) {
      return Consumer(
        builder: (context, ref, child) {
          final summaryAsync = ref.watch(bookAiSummaryProvider(book.id));

          return summaryAsync.when(
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (err, stack) => Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('Không thể tải tóm tắt AI: $err'),
                  ElevatedButton(
                    onPressed: () => ref.refresh(bookAiSummaryProvider(book.id)),
                    child: const Text('Thử lại'),
                  ),
                ],
              ),
            ),
            data: (response) {
              if (response.status == 'failed') {
                return Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(response.errorMessage ?? 'Tạo tóm tắt AI thất bại'),
                      const SizedBox(height: 12),
                      ElevatedButton(
                        onPressed: () {
                          ref.read(bookAiSummaryControllerProvider).regenerate(book.id);
                        },
                        child: const Text('Tạo lại bản tóm tắt'),
                      ),
                    ],
                  ),
                );
              }

              // Khi status == 'completed', hiển thị các Card dữ liệu đã máp ở Phần 2
              return BuildSummarySheetContent(response: response, book: book);
            },
          );
        },
      );
    },
  );
}
```
