///////////////////// /api/v1/books

```json
[
  {
    "id": "5ef640e3-40f5-4fa6-8343-b6fd6a03c305",
    "title": "trr",
    "author": null,
    "total_sections": 122,
    "total_units": 4,
    "status": "ready",
    "document_type": "docx",
    "file_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/raw_books/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/original.docx",
    "created_at": "2026-05-28T17:27:17.320381Z",
    "updated_at": "2026-05-28T17:34:21.967157Z"
  },
  {
    "id": "b9b44cbe-9941-48d3-9dc0-d081220c2edd",
    "title": "Chương 4_ Phương pháp luận nghiên cứu",
    "author": null,
    "total_sections": 3,
    "total_units": 3,
    "status": "ready",
    "document_type": "pdf",
    "file_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/raw_books/b9b44cbe-9941-48d3-9dc0-d081220c2edd/original.pdf",
    "created_at": "2026-05-28T17:15:24.080262Z",
    "updated_at": "2026-05-28T17:27:08.605209Z"
  },
  {
    "id": "f4463cd7-32fd-4de9-bf50-f61474eb5b54",
    "title": "phase5_sample",
    "author": null,
    "total_sections": 2,
    "total_units": 1,
    "status": "ready",
    "document_type": "epub",
    "file_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/raw_books/f4463cd7-32fd-4de9-bf50-f61474eb5b54/original.epub",
    "created_at": "2026-05-28T17:34:27.238465Z",
    "updated_at": "2026-05-28T17:34:59.942425Z"
  }
]
```

///////////////////// /api/v1/books/{book_id}

```json
{
  "id": "5ef640e3-40f5-4fa6-8343-b6fd6a03c305",
  "title": "trr",
  "author": null,
  "total_sections": 122,
  "total_units": 4,
  "status": "ready",
  "document_type": "docx",
  "file_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/raw_books/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/original.docx",
  "created_at": "2026-05-28T17:27:17.320381Z",
  "updated_at": "2026-05-28T17:34:21.967157Z"
}
```

///////////////////// /api/v1/books/{book_id}/details

```json
{
  "book_id": "5ef640e3-40f5-4fa6-8343-b6fd6a03c305",
  "book_status": "ready",
  "mode": "pareto",
  "total_sections": 122,
  "total_units": 4,
  "units": [
    {
      "id": "6e7f8eea-29b5-4447-83ec-3aec02096e58",
      "title": "LOGIC MỆNH ĐỀ - Phần 1/2",
      "status": "ready",
      "unit_index": 0,
      "unit_type": "pareto_focus",
      "source_text_char_count": 14147,
      "estimated_audio_seconds": 1515,
      "main_segment_count": 6,
      "review_text": "Trong phần này, chúng ta đã tìm hiểu về mệnh đề toán học, định nghĩa là phát biểu có chân trị đúng hoặc sai. Mệnh đề có thể là sơ cấp hoặc phức hợp, được phân tích bằng bảng chân trị. Các phép toán logic cơ bản gồm phủ định, và, hoặc, kéo theo, và tương đương, mỗi phép có quy tắc chân trị riêng. Biểu thức logic được xây dựng từ các mệnh đề và phép toán, và hai biểu thức được coi là tương đương logic nếu chúng có cùng chân trị. Chúng ta cũng đã khám phá vị từ, là hàm biến thành mệnh đề khi gán giá trị, và các lượng từ phổ dụng, tồn tại. Cuối cùng, suy luận logic và chứng minh là quá trình xác định tính đúng đắn của các khẳng định dựa trên các luật và quy tắc suy diễn như Modus Ponens và Modus Tollens.",
      "review_audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_1/pareto/review.mp3",
      "planner_reason": "Tách từ nhóm lớn thành phần 1/2 để không vượt giới hạn xử lý.",
      "segments": [
        {
          "id": 83,
          "segment_index": 0,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_1/pareto/part_1.mp3",
          "text_content": "Mệnh đề toán học là những phát biểu diễn đạt một ý tưởng trọn vẹn, có thể khẳng định một cách khách quan là đúng hoặc sai, không thể vừa đúng vừa sai. Chúng ta thường dùng các ký tự như p, q, r để ký hiệu các mệnh đề. Giá trị đúng hoặc sai của mệnh đề được gọi là chân trị, với đúng ký hiệu là một và sai ký hiệu là không. Những phát biểu không xác định được tính đúng sai, như ý kiến cá nhân hay câu hỏi, thì không phải là mệnh đề.",
          "duration_ms": 26280
        },
        {
          "id": 84,
          "segment_index": 1,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_1/pareto/part_2.mp3",
          "text_content": "Mệnh đề được chia thành hai loại chính. Mệnh đề sơ cấp là những mệnh đề không thể phân tích thành các mệnh đề đơn giản hơn bằng các phép toán logic. Ngược lại, mệnh đề phức hợp được tạo thành từ hai hoặc nhiều mệnh đề khác thông qua các phép toán logic như phủ định, và, hoặc. Để xác định chân trị của mệnh đề phức hợp, chúng ta sử dụng bảng chân trị, một công cụ biểu diễn chân trị của mệnh đề phức hợp dựa trên chân trị của các mệnh đề sơ cấp cấu thành.",
          "duration_ms": 25776
        },
        {
          "id": 85,
          "segment_index": 2,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_1/pareto/part_3.mp3",
          "text_content": "Các phép toán logic cơ bản bao gồm phủ định, là phép toán một ngôi đảo ngược chân trị của mệnh đề. Ngoài ra, có các phép toán hai ngôi như phép nối liền, hay còn gọi là phép và, chỉ đúng khi cả hai mệnh đề đều đúng. Phép nối rời, hay phép hoặc, đúng khi ít nhất một trong hai mệnh đề đúng. Phép hoặc loại trừ đúng khi hai mệnh đề có chân trị khác nhau. Phép kéo theo, hay phép điều kiện, chỉ sai khi mệnh đề đầu đúng và mệnh đề sau sai. Cuối cùng, phép tương đương đúng khi hai mệnh đề có cùng chân trị.",
          "duration_ms": 32016
        },
        {
          "id": 86,
          "segment_index": 3,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_1/pareto/part_4.mp3",
          "text_content": "Biểu thức logic được xây dựng từ các mệnh đề, hằng logic, biến mệnh đề, các phép toán logic và dấu ngoặc. Hai biểu thức logic được gọi là tương đương logic nếu chúng có cùng chân trị trong mọi trường hợp, tức là biểu thức tương đương giữa chúng là một hằng đúng. Các luật logic cơ bản như luật phủ định, giao hoán, kết hợp, phân bố, De Morgan, và luật về phần tử bù là nền tảng để biến đổi và chứng minh sự tương đương giữa các biểu thức logic.",
          "duration_ms": 26496
        },
        {
          "id": 87,
          "segment_index": 4,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_1/pareto/part_5.mp3",
          "text_content": "Vị từ là một hàm phụ thuộc vào các biến, mà khi gán giá trị cho các biến, nó trở thành một mệnh đề. Các biến này được gọi là biến tự do. Lượng từ được sử dụng để xây dựng các mệnh đề từ vị từ. Lượng từ phổ dụng, ký hiệu là với mọi x, có nghĩa là mệnh đề đúng với tất cả các giá trị của x trong miền xác định. Lượng từ tồn tại, ký hiệu là tồn tại x, có nghĩa là mệnh đề đúng với ít nhất một giá trị của x trong miền xác định. Việc phủ định các lượng từ cũng tuân theo các quy tắc cụ thể, ví dụ, phủ định của với mọi x p(x) là tồn tại x không p(x).",
          "duration_ms": 36408
        },
        {
          "id": 88,
          "segment_index": 5,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_1/pareto/part_6.mp3",
          "text_content": "Trong logic, định lý là một khẳng định đã được chứng minh là đúng. Một lập luận chỉ ra tính đúng đắn của định lý được gọi là chứng minh. Suy diễn logic xảy ra khi một tập hợp các giả thuyết dẫn đến một kết luận mà biểu thức kéo theo giữa chúng là hằng đúng. Các phương pháp chứng minh bao gồm lập bảng chân trị, sử dụng các luật logic, và áp dụng các luật suy diễn đã biết. Một số luật suy diễn quan trọng là Modus Ponens, Modus Tollens, quy tắc tam đoạn luận, và quy tắc phản chứng, giúp chúng ta xây dựng các lập luận chặt chẽ và hợp lệ.",
          "duration_ms": 31800
        }
      ]
    },
    {
      "id": "056ebc7c-936d-4bd7-af6c-7c1062abaec2",
      "title": "LOGIC MỆNH ĐỀ - Phần 2/2",
      "status": "ready",
      "unit_index": 1,
      "unit_type": "pareto_focus",
      "source_text_char_count": 7847,
      "estimated_audio_seconds": 790,
      "main_segment_count": 11,
      "review_text": "Trong phần này, chúng ta đã tìm hiểu về các mô hình suy diễn trong logic, phân biệt giữa suy diễn đúng và sai qua các ví dụ cụ thể. Chúng ta cũng khám phá các phương pháp chứng minh quan trọng như phản chứng và chứng minh theo trường hợp. Đặc biệt, nguyên lý quy nạp được giới thiệu chi tiết với hai dạng: quy nạp yếu và quy nạp mạnh, cùng các bước cơ sở và quy nạp. Các ví dụ áp dụng quy nạp đã minh họa cách chứng minh các công thức tổng, tính chia hết, và các tính chất toán học khác. Điểm mấu chốt là hiểu rõ cách xây dựng một lập luận logic và các kỹ thuật chứng minh cơ bản.",
      "review_audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/review.mp3",
      "planner_reason": "Tách từ nhóm lớn thành phần 2/2 để không vượt giới hạn xử lý.",
      "segments": [
        {
          "id": 89,
          "segment_index": 0,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_1.mp3",
          "text_content": "Trong logic học, chúng ta có thể chứng minh tính đúng đắn của các mô hình suy diễn. Ví dụ, mô hình với các giả thuyết p, q kéo theo r, và p kéo theo s, cùng với giả thuyết q, có thể suy ra s kéo theo r. Đây là một suy diễn hợp lệ.",
          "duration_ms": 15720
        },
        {
          "id": 90,
          "segment_index": 1,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_2.mp3",
          "text_content": "Một biểu thức logic như 'mở ngoặc p và q đóng ngoặc và mở ngoặc q kéo theo r đóng ngoặc và r đóng ngoặc kéo theo p' được chứng minh là một luật suy diễn, hay còn gọi là hằng đúng, thông qua việc lập bảng chân trị.",
          "duration_ms": 12000
        },
        {
          "id": 91,
          "segment_index": 2,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_3.mp3",
          "text_content": "Tuy nhiên, không phải mọi suy diễn đều đúng. Chẳng hạn, khi xét một chương trình, nếu nó thành công thì phải bắt đầu và kết thúc. Nhưng nếu chương trình đã bắt đầu và không thành công, chúng ta không thể kết luận rằng chương trình đã không kết thúc. Suy diễn này là không hợp lệ.",
          "duration_ms": 16224
        },
        {
          "id": 92,
          "segment_index": 3,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_4.mp3",
          "text_content": "Ngược lại, một suy diễn khác lại hoàn toàn đúng đắn. Nếu A được lên chức và làm việc nhiều thì A được tăng lương. Nếu được tăng lương, A sẽ mua xe mới. Mà A không mua xe mới. Từ đó, chúng ta có thể suy ra rằng A không được lên chức hoặc A không làm việc nhiều.",
          "duration_ms": 17304
        },
        {
          "id": 93,
          "segment_index": 4,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_5.mp3",
          "text_content": "Ngoài ra, có nhiều phương pháp chứng minh khác nhau. Phương pháp phản chứng dựa trên luật suy diễn 'p kéo theo q tương đương với không q kéo theo không p'. Để chứng minh một mệnh đề p kéo theo q, ta giả sử p và không q là đúng, rồi chỉ ra điều này dẫn đến mâu thuẫn. Ví dụ, để chứng minh tổng hai số nguyên lẻ là một số chẵn, ta giả sử tổng đó là số lẻ và tìm ra mâu thuẫn.",
          "duration_ms": 23448
        },
        {
          "id": 94,
          "segment_index": 5,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_6.mp3",
          "text_content": "Một phương pháp khác là chứng minh theo trường hợp. Phương pháp này được dùng để chứng minh một mệnh đề đúng với mọi phần tử trong một tập hợp bằng cách chia tập hợp đó thành các trường hợp riêng biệt. Chẳng hạn, để chứng minh rằng với mọi số tự nhiên n, n mũ ba cộng n là số chẵn, ta xét hai trường hợp: n là số chẵn và n là số lẻ.",
          "duration_ms": 20496
        },
        {
          "id": 95,
          "segment_index": 6,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_7.mp3",
          "text_content": "Trong toán học, tập hợp số tự nhiên N bao gồm các số không, một, hai, ba, và tiếp tục. Đây là một tập hợp được sắp xếp toàn phần, nghĩa là mọi tập con không rỗng của N đều có một phần tử nhỏ nhất duy nhất.",
          "duration_ms": 13800
        },
        {
          "id": 96,
          "segment_index": 7,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_8.mp3",
          "text_content": "Nguyên lý quy nạp là một công cụ mạnh mẽ để chứng minh các mệnh đề p(n) đúng với mọi số tự nhiên n lớn hơn hoặc bằng một giá trị n không xác định. Nó bao gồm hai bước chính: bước cơ sở và bước quy nạp.",
          "duration_ms": 13368
        },
        {
          "id": 97,
          "segment_index": 8,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_9.mp3",
          "text_content": "Bước cơ sở yêu cầu kiểm tra mệnh đề p(n không) là đúng. Bước quy nạp có hai dạng: quy nạp yếu và quy nạp mạnh. Quy nạp yếu chứng minh rằng nếu p(k) đúng thì p(k cộng một) cũng đúng. Còn quy nạp mạnh thì chứng minh rằng nếu tất cả các mệnh đề từ p(n không) đến p(k) đều đúng, thì p(k cộng một) cũng đúng.",
          "duration_ms": 24984
        },
        {
          "id": 98,
          "segment_index": 9,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_10.mp3",
          "text_content": "Nguyên lý quy nạp được áp dụng để chứng minh nhiều công thức và tính chất. Ví dụ, chúng ta có thể chứng minh công thức tổng các bình phương xen kẽ dấu từ một bình phương trừ hai bình phương đến n bình phương. Hoặc chứng minh công thức tổng các phân số dạng i chia cho i cộng một giai thừa.",
          "duration_ms": 15984
        },
        {
          "id": 99,
          "segment_index": 10,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/part_11.mp3",
          "text_content": "Một ứng dụng khác là chứng minh mệnh đề 'bảy mũ n trừ một' chia hết cho sáu với mọi n lớn hơn hoặc bằng một. Hay chứng minh rằng 'n mũ năm trừ n' chia hết cho năm với mọi n lớn hơn hoặc bằng một, từ đó suy ra 'ba mươi bảy mũ năm trăm trừ ba mươi bảy mũ một trăm' chia hết cho mười.",
          "duration_ms": 16752
        }
      ]
    },
    {
      "id": "bbbbeab0-6d43-4a69-9836-6f8ebe8275a7",
      "title": "PHÉP ĐẾM - Phần 1/2",
      "status": "ready",
      "unit_index": 2,
      "unit_type": "pareto_focus",
      "source_text_char_count": 14250,
      "estimated_audio_seconds": 1592,
      "main_segment_count": 22,
      "review_text": "Trong phần này, chúng ta đã tìm hiểu về các khái niệm cơ bản của tập hợp, bao gồm định nghĩa, cách biểu diễn, các quan hệ như tập con và tập bằng nhau. Chúng ta cũng đã nắm vững các phép toán trên tập hợp như hợp, giao, hiệu, và phần bù, cùng với các tính chất quan trọng của chúng. Tiếp theo, chúng ta khám phá khái niệm ánh xạ, các loại ánh xạ như đơn ánh, toàn ánh, song ánh, và các phép toán trên ánh xạ. Phần cuối cùng tập trung vào các tập số cơ bản, phép chia hết, ước số chung lớn nhất, bội số chung nhỏ nhất, số nguyên tố và các định lý liên quan. Cuối cùng, chúng ta đã học ba nguyên lý đếm cốt lõi: nguyên lý nhân, nguyên lý cộng và nguyên lý bù trừ, cùng với các ứng dụng của chúng trong việc giải quyết các bài toán đếm.",
      "review_audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/review.mp3",
      "planner_reason": "Tách từ nhóm lớn thành phần 1/2 để không vượt giới hạn xử lý.",
      "segments": [
        {
          "id": 116,
          "segment_index": 0,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_1.mp3",
          "text_content": "Trong toán học, tập hợp được hiểu là một tụ tập các đối tượng, gọi là phần tử. Đây là một khái niệm nguyên thủy, không định nghĩa, mà tồn tại theo các tiên đề chặt chẽ. Chúng ta thường dùng các chữ cái in hoa như A, B để đặt tên cho tập hợp. Nếu một phần tử 'a' thuộc tập hợp A, ta ký hiệu là 'a thuộc A'; ngược lại, nếu không thuộc, ta ký hiệu 'a không thuộc A'.",
          "duration_ms": 23376
        },
        {
          "id": 117,
          "segment_index": 1,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_2.mp3",
          "text_content": "Một tập hợp có thể là phần tử của tập hợp khác, tạo thành họ tập hợp. Có tập hợp rỗng, ký hiệu là ∅, không chứa phần tử nào. Ngược lại, tập vũ trụ U chứa tất cả các phần tử của các tập con đang xét. Các tập hợp có ít nhất một phần tử được gọi là tập hợp không rỗng.",
          "duration_ms": 17208
        },
        {
          "id": 118,
          "segment_index": 2,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_3.mp3",
          "text_content": "Tập hợp có thể được biểu diễn bằng cách liệt kê tất cả các phần tử giữa hai dấu ngoặc nhọn, ví dụ {a, b, c}. Hoặc bằng cách nêu đặc trưng của phần tử, tức là mô tả tính chất mà các phần tử trong tập hợp đó phải thỏa mãn, ví dụ {x thuộc R sao cho x bình phương cộng hai x trừ ba bằng không}. Ngoài ra, biểu đồ Venn cũng là một cách biểu diễn hình học trực quan.",
          "duration_ms": 23208
        },
        {
          "id": 119,
          "segment_index": 3,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_4.mp3",
          "text_content": "Về quan hệ, nếu mọi phần tử của tập hợp A đều là phần tử của tập hợp B, thì A là tập hợp con của B, ký hiệu A ⊆ B. Hai tập hợp A và B bằng nhau khi và chỉ khi A là tập con của B và B là tập con của A. Tập rỗng và chính nó là các tập con tầm thường của mọi tập hợp. Nếu B là tập con của A nhưng khác A, thì B là tập con thực sự của A.",
          "duration_ms": 20880
        },
        {
          "id": 120,
          "segment_index": 4,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_5.mp3",
          "text_content": "Các phép toán cơ bản trên tập hợp bao gồm: Hợp của A và B, ký hiệu A ∪ B, là tập hợp gồm tất cả các phần tử thuộc ít nhất một trong hai tập hợp. Giao của A và B, ký hiệu A ∩ B, là tập hợp các phần tử vừa thuộc A, vừa thuộc B.",
          "duration_ms": 15984
        },
        {
          "id": 121,
          "segment_index": 5,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_6.mp3",
          "text_content": "Hiệu của tập hợp A với tập hợp B, ký hiệu A \\ B, là tập hợp các phần tử thuộc A nhưng không thuộc B. Cần lưu ý rằng A \\ B khác B \\ A. Phần bù của A trong B, ký hiệu C_B A hoặc A mũ c, là hiệu của B với A khi A là tập con của B. Khi xét trong tập vũ trụ U, ta thường ký hiệu đơn giản là A mũ c.",
          "duration_ms": 18936
        },
        {
          "id": 122,
          "segment_index": 6,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_7.mp3",
          "text_content": "Các phép toán trên tập hợp có nhiều tính chất quan trọng như giao hoán, kết hợp, phân bố và luật De Morgan. Ví dụ, luật De Morgan phát biểu rằng phần bù của hợp hai tập hợp bằng giao các phần bù của chúng, và phần bù của giao hai tập hợp bằng hợp các phần bù của chúng.",
          "duration_ms": 15576
        },
        {
          "id": 123,
          "segment_index": 7,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_8.mp3",
          "text_content": "Tích Descartes của hai tập hợp A và B, ký hiệu A × B, là tập hợp tất cả các cặp có thứ tự (a, b) với a thuộc A và b thuộc B. Số phần tử của tích Descartes A × B bằng tích số phần tử của A và B. Khái niệm này có thể mở rộng cho nhiều tập hợp.",
          "duration_ms": 15888
        },
        {
          "id": 124,
          "segment_index": 8,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_9.mp3",
          "text_content": "Ánh xạ từ tập X vào tập Y là một quy tắc tương ứng mỗi phần tử của X với duy nhất một phần tử của Y. Phần tử tương ứng được gọi là ảnh. Chúng ta cũng có khái niệm ảnh ngược của một phần tử hoặc một tập hợp.",
          "duration_ms": 11736
        },
        {
          "id": 125,
          "segment_index": 9,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_10.mp3",
          "text_content": "Có ba loại ánh xạ chính: Đơn ánh, khi mỗi phần tử của Y có tối đa một phần tử của X tương ứng. Toàn ánh, khi mỗi phần tử của Y đều có ít nhất một phần tử của X tương ứng. Và Song ánh, là ánh xạ vừa đơn ánh vừa toàn ánh. Ngoài ra, còn có ánh xạ ngược và ánh xạ hợp, được tạo thành từ việc kết hợp hai ánh xạ liên tiếp.",
          "duration_ms": 21576
        },
        {
          "id": 126,
          "segment_index": 10,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_11.mp3",
          "text_content": "Các tập số cơ bản bao gồm số tự nhiên N, số nguyên Z, số hữu tỉ Q, số thực R và số phức C. Trên các tập số này, chúng ta thực hiện các phép toán cộng và nhân với các tính chất như giao hoán, kết hợp, có phần tử trung hòa là không cho phép cộng và một cho phép nhân, cùng với phần tử đối cho phép cộng và tính phân phối giữa nhân và cộng.",
          "duration_ms": 20832
        },
        {
          "id": 127,
          "segment_index": 11,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_12.mp3",
          "text_content": "Đối với các tập con của số nguyên Z, nếu một tập con không rỗng và bị chặn trên, nó có phần tử lớn nhất duy nhất. Tương tự, nếu bị chặn dưới, nó có phần tử nhỏ nhất duy nhất. Với tập con của số tự nhiên N, mọi tập con không rỗng đều có phần tử nhỏ nhất duy nhất.",
          "duration_ms": 17544
        },
        {
          "id": 128,
          "segment_index": 12,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_13.mp3",
          "text_content": "Với hai số nguyên a và b khác không, ta luôn có thể biểu diễn a bằng b nhân q cộng r, trong đó q là thương và r là số dư, với r lớn hơn hoặc bằng không và nhỏ hơn giá trị tuyệt đối của b. Nếu số dư r bằng không, ta nói a chia hết cho b, hay b là ước của a, và a là bội của b.",
          "duration_ms": 18336
        },
        {
          "id": 129,
          "segment_index": 13,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_14.mp3",
          "text_content": "Ước số chung lớn nhất của hai số nguyên dương a và b, ký hiệu là (a, b), là giá trị lớn nhất trong tập các ước chung của chúng. Nếu (a, b) bằng một, ta nói a và b là nguyên tố cùng nhau. Bội số chung nhỏ nhất của a và b, ký hiệu là BSCNN của a, b, là giá trị nhỏ nhất trong tập các bội chung của chúng. Một định lý quan trọng là tích của ước số chung lớn nhất và bội số chung nhỏ nhất của hai số bằng tích của hai số đó.",
          "duration_ms": 28944
        },
        {
          "id": 130,
          "segment_index": 14,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_15.mp3",
          "text_content": "Số nguyên dương n được gọi là nguyên tố nếu n lớn hơn một và chỉ có hai ước số dương là một và chính nó. Một định nghĩa khác là số nguyên n là nguyên tố nếu n khác cộng trừ một và nếu n chia hết cho tích của hai số nguyên a và b, thì n phải chia hết cho a hoặc n chia hết cho b.",
          "duration_ms": 17616
        },
        {
          "id": 131,
          "segment_index": 15,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_16.mp3",
          "text_content": "Một hệ quả là nếu n là số nguyên tố và n chia hết cho tích của nhiều số, thì n phải chia hết cho ít nhất một trong các số đó. Định lý cơ bản của số học khẳng định rằng mọi số nguyên khác không đều có thể biểu diễn duy nhất dưới dạng tích các thừa số nguyên tố. Ngoài ra, định lý Fermat nhỏ phát biểu rằng nếu p là số nguyên tố và a là số nguyên dương, thì a mũ p đồng dư với a theo modulo p.",
          "duration_ms": 23880
        },
        {
          "id": 132,
          "segment_index": 16,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_17.mp3",
          "text_content": "Nguyên lý nhân được sử dụng để đếm số cách thực hiện một chuỗi các công việc độc lập. Nếu có k công việc cần thực hiện liên tiếp, và công việc thứ i có m_i cách chọn, thì tổng số cách thực hiện k công việc đó là tích của tất cả các m_i. Nguyên lý này giúp giải quyết các bài toán như tìm số ước số nguyên dương của một số, số cách ghi nhãn các đối tượng, hoặc số lượng xâu nhị phân có độ dài n.",
          "duration_ms": 23088
        },
        {
          "id": 133,
          "segment_index": 17,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_18.mp3",
          "text_content": "Ví dụ, số ánh xạ từ một tập có m phần tử vào một tập có n phần tử là n mũ m. Số đơn ánh từ một tập có m phần tử vào một tập có n phần tử là tích của n nhân n trừ một nhân... nhân n trừ m cộng một. Trong ngôn ngữ tập hợp, nguyên lý nhân phát biểu rằng số phần tử của tích Descartes của các tập hợp hữu hạn bằng tích số phần tử của từng tập thành phần.",
          "duration_ms": 22104
        },
        {
          "id": 134,
          "segment_index": 18,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_19.mp3",
          "text_content": "Nguyên lý cộng áp dụng khi chúng ta có nhiều lựa chọn công việc mà chỉ cần thực hiện một trong số đó. Nếu có k công việc không thể thực hiện đồng thời, và công việc thứ i có m_i cách chọn, thì tổng số cách chọn một công việc là tổng của tất cả các m_i. Ví dụ, một sinh viên có thể chọn bài thực hành từ ba danh sách khác nhau, số cách chọn sẽ là tổng số bài trong mỗi danh sách.",
          "duration_ms": 22032
        },
        {
          "id": 135,
          "segment_index": 19,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_20.mp3",
          "text_content": "Dưới dạng tập hợp, nếu các tập hợp là đôi một rời nhau, thì số phần tử của hợp các tập hợp này bằng tổng số phần tử của từng tập thành phần.",
          "duration_ms": 8376
        },
        {
          "id": 136,
          "segment_index": 20,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_21.mp3",
          "text_content": "Khi hai công việc có thể được làm đồng thời, chúng ta sử dụng nguyên lý bù trừ. Đối với hai tập hợp hữu hạn A1 và A2, số phần tử của hợp A1 hợp A2 bằng số phần tử của A1 cộng số phần tử của A2 trừ đi số phần tử của giao A1 giao A2. Công thức này có thể mở rộng cho ba tập hợp và nhiều hơn nữa.",
          "duration_ms": 19488
        },
        {
          "id": 137,
          "segment_index": 21,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/part_22.mp3",
          "text_content": "Nguyên lý bù trừ cũng cho phép chúng ta tính số phần tử không thỏa mãn bất kỳ tính chất nào trong một tập vũ trụ hữu hạn. Một ứng dụng điển hình là bài toán đếm số cách bỏ n lá thư vào n phong bì sao cho không lá thư nào đúng địa chỉ.",
          "duration_ms": 13464
        }
      ]
    },
    {
      "id": "2837a054-6d57-4533-91f5-6f3850f2aada",
      "title": "PHÉP ĐẾM - Phần 2/2",
      "status": "ready",
      "unit_index": 3,
      "unit_type": "pareto_focus",
      "source_text_char_count": 13021,
      "estimated_audio_seconds": 1392,
      "main_segment_count": 16,
      "review_text": "Trong phần này, chúng ta đã tìm hiểu về các nguyên lý đếm cơ bản. Đầu tiên là Nguyên lý Dirichlet, với hai dạng: cơ bản và tổng quát, giúp xác định sự tồn tại của ít nhất một phần tử thỏa mãn điều kiện khi phân bổ. Tiếp theo, chúng ta khám phá Chỉnh hợp, Hoán vị và Tổ hợp, phân biệt chúng dựa trên yếu tố thứ tự và sự khác biệt của các phần tử được chọn. Cuối cùng, chúng ta tìm hiểu về Chỉnh hợp lặp và Tổ hợp lặp, cho phép các phần tử được chọn có thể giống nhau. Nắm vững các định nghĩa và công thức này là chìa khóa để giải quyết các bài toán đếm trong nhiều lĩnh vực.",
      "review_audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/review.mp3",
      "planner_reason": "Tách từ nhóm lớn thành phần 2/2 để không vượt giới hạn xử lý.",
      "segments": [
        {
          "id": 100,
          "segment_index": 0,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_1.mp3",
          "text_content": "Nguyên lý Dirichlet, hay còn gọi là nguyên lý chuồng bồ câu, phát biểu rằng: nếu có k cộng một hoặc nhiều hơn đồ vật được đặt vào trong k hộp, thì tồn tại ít nhất một hộp chứa hai đồ vật trở lên.",
          "duration_ms": 11280
        },
        {
          "id": 101,
          "segment_index": 1,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_2.mp3",
          "text_content": "Ví dụ, trong bất kỳ nhóm ba trăm sáu mươi bảy người nào, chắc chắn có ít nhất hai người có cùng ngày sinh nhật, vì chỉ có tối đa ba trăm sáu mươi sáu ngày sinh nhật khác nhau.",
          "duration_ms": 9888
        },
        {
          "id": 102,
          "segment_index": 2,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_3.mp3",
          "text_content": "Nguyên lý Dirichlet tổng quát mở rộng rằng: nếu có N đồ vật được đặt vào trong k hộp, thì sẽ tồn tại một hộp chứa ít nhất giá trị hàm trần của N chia k đồ vật.",
          "duration_ms": 9624
        },
        {
          "id": 103,
          "segment_index": 3,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_4.mp3",
          "text_content": "Hàm trần của x là số nguyên nhỏ nhất lớn hơn hoặc bằng x. Chẳng hạn, trong một trăm người, sẽ có ít nhất chín người sinh cùng một tháng, vì một trăm chia mười hai, lấy hàm trần, bằng chín.",
          "duration_ms": 11472
        },
        {
          "id": 104,
          "segment_index": 4,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_5.mp3",
          "text_content": "Chỉnh hợp chập k của n phần tử là một phép chọn k phần tử từ n phần tử có sẵn, với hai tính chất quan trọng: có thứ tự và các phần tử đều khác nhau.",
          "duration_ms": 9744
        },
        {
          "id": 105,
          "segment_index": 5,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_6.mp3",
          "text_content": "Công thức tính số chỉnh hợp chập k của n phần tử là A n k bằng n giai thừa chia cho n trừ k tất cả giai thừa.",
          "duration_ms": 7584
        },
        {
          "id": 106,
          "segment_index": 6,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_7.mp3",
          "text_content": "Ví dụ, để chọn một Ban cán sự lớp gồm ba người từ năm mươi sinh viên, với các vị trí lớp trưởng, lớp phó học tập và lớp phó phong trào, ta có A năm mươi ba bằng năm mươi nhân bốn mươi chín nhân bốn mươi tám, tức là một trăm mười bảy ngàn sáu trăm cách.",
          "duration_ms": 14256
        },
        {
          "id": 107,
          "segment_index": 7,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_8.mp3",
          "text_content": "Hoán vị là một trường hợp đặc biệt của chỉnh hợp khi số phần tử được chọn k bằng tổng số phần tử n. Nó là cách sắp xếp n phần tử khác nhau theo một thứ tự nhất định.",
          "duration_ms": 9528
        },
        {
          "id": 108,
          "segment_index": 8,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_9.mp3",
          "text_content": "Công thức tính số hoán vị của n phần tử là P n bằng n giai thừa. Chẳng hạn, để đánh số báo danh và xếp chỗ ngồi cho ba mươi thí sinh trong một phòng thi, ta có P ba mươi bằng ba mươi giai thừa cách.",
          "duration_ms": 12504
        },
        {
          "id": 109,
          "segment_index": 9,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_10.mp3",
          "text_content": "Tổ hợp chập k của n phần tử là một phép chọn k phần tử từ n phần tử có sẵn, với tính chất các phần tử được chọn đều khác nhau nhưng không có thứ tự.",
          "duration_ms": 9048
        },
        {
          "id": 110,
          "segment_index": 10,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_11.mp3",
          "text_content": "Công thức tính số tổ hợp chập k của n phần tử là C n k bằng n giai thừa chia cho k giai thừa nhân với n trừ k tất cả giai thừa.",
          "duration_ms": 8544
        },
        {
          "id": 111,
          "segment_index": 11,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_12.mp3",
          "text_content": "Ví dụ, trong một giải đấu mười đội bóng thi đấu vòng tròn một lượt, số trận đấu cần tổ chức là C mười hai bằng bốn mươi lăm trận.",
          "duration_ms": 7584
        },
        {
          "id": 112,
          "segment_index": 12,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_13.mp3",
          "text_content": "Chỉnh hợp lặp chập k của n phần tử là phép chọn k phần tử từ n phần tử, trong đó các phần tử có thể giống nhau và có thứ tự.",
          "duration_ms": 8208
        },
        {
          "id": 113,
          "segment_index": 13,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_14.mp3",
          "text_content": "Công thức tính số chỉnh hợp lặp chập k của n phần tử là n mũ k. Ví dụ, để tạo các số điện thoại bảy chữ số từ các chữ số không đến chín, ta có mười mũ bảy, tức là mười triệu số điện thoại khác nhau.",
          "duration_ms": 12672
        },
        {
          "id": 114,
          "segment_index": 14,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_15.mp3",
          "text_content": "Tổ hợp lặp chập k của n phần tử là cách chọn k phần tử từ n phần tử, trong đó các phần tử có thể giống nhau nhưng không có thứ tự.",
          "duration_ms": 8112
        },
        {
          "id": 115,
          "segment_index": 15,
          "audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/part_16.mp3",
          "text_content": "Công thức tính số tổ hợp lặp chập k của n phần tử là C của n cộng k trừ một, chập k. Ví dụ, có bao nhiêu cách chọn bảy món quà từ bốn loại quà khác nhau A, B, C, D? Đó là C của bốn cộng bảy trừ một, chập bảy, tức là C mười bảy, bằng một trăm hai mươi cách chọn.",
          "duration_ms": 18576
        }
      ]
    }
  ]
}
```

///////////////////// /api/v1/books/{book_id}/outline

```json
{
  "book_id": "5ef640e3-40f5-4fa6-8343-b6fd6a03c305",
  "total_sections": 122,
  "outline_tree": [
    {
      "id": "127cbb16-5571-45cc-9955-20bb0df5630f",
      "title": "LOGIC MỆNH ĐỀ",
      "level": 1,
      "path": "1",
      "page_start": null,
      "page_end": null,
      "text_char_count": 0,
      "children": [
        {
          "id": "b84fe2b8-9bbf-4237-9064-3682ade567e1",
          "title": "Mệnh đề",
          "level": 2,
          "path": "1.1",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "1c214625-8db0-4183-bbd1-097fc08549d7",
              "title": "Khái niệm mệnh đề và chân trị",
              "level": 3,
              "path": "1.1.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1198,
              "children": []
            },
            {
              "id": "7c0ff62f-22ef-4a30-8062-af860b319a8d",
              "title": "Phân loại",
              "level": 3,
              "path": "1.1.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 642,
              "children": []
            },
            {
              "id": "dbe5b18b-6349-4080-88b1-814d73d4e862",
              "title": "Các phép toán mệnh đề",
              "level": 3,
              "path": "1.1.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1562,
              "children": [
                {
                  "id": "56c6f5a4-0dcf-4649-a45b-2b3e527c0026",
                  "title": "Phép tuyển ()",
                  "level": 4,
                  "path": "1.1.3.1",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 401,
                  "children": []
                },
                {
                  "id": "32fcf57c-42ba-447e-a7a6-cc1e3f7cb370",
                  "title": "Phép hoặc ()",
                  "level": 4,
                  "path": "1.1.3.2",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 329,
                  "children": []
                },
                {
                  "id": "5cefac2c-a9bd-4a0a-b8a1-aa31816e97b3",
                  "title": "Phép kéo theo()",
                  "level": 4,
                  "path": "1.1.3.3",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 773,
                  "children": []
                },
                {
                  "id": "4a1b843a-8cc0-460d-bddc-7a4d4c453bb8",
                  "title": "Phép kéo theo hai chiều hay tương đương ()",
                  "level": 4,
                  "path": "1.1.3.4",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 348,
                  "children": []
                }
              ]
            },
            {
              "id": "a4396c76-5af5-4f1b-b747-d6e187672c9e",
              "title": "Biểu Thức Logic",
              "level": 3,
              "path": "1.1.4",
              "page_start": null,
              "page_end": null,
              "text_char_count": 0,
              "children": [
                {
                  "id": "e7bee644-1b5c-480b-adb7-176c454f132a",
                  "title": "Khái niệm",
                  "level": 4,
                  "path": "1.1.4.1",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 154,
                  "children": []
                },
                {
                  "id": "ffce7339-8a22-4cb5-82f7-2413b270583a",
                  "title": "Các ví dụ",
                  "level": 4,
                  "path": "1.1.4.2",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 161,
                  "children": []
                },
                {
                  "id": "fb30a994-06f2-47b6-a1be-16e3293a6f07",
                  "title": "Sự tương đương logic",
                  "level": 4,
                  "path": "1.1.4.3",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 431,
                  "children": []
                },
                {
                  "id": "fb1b33fa-0799-4440-80c9-42cc6e9344cd",
                  "title": "Các luật logic thông dụng",
                  "level": 4,
                  "path": "1.1.4.4",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 711,
                  "children": []
                },
                {
                  "id": "3b8c23e1-a3f9-45b8-bef4-f87c2aa1a13c",
                  "title": "Các qui tắc thay thế",
                  "level": 4,
                  "path": "1.1.4.5",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 314,
                  "children": []
                },
                {
                  "id": "ad26b5c4-380b-4592-a578-da6a3ba93d47",
                  "title": "Các ví dụ",
                  "level": 4,
                  "path": "1.1.4.6",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 1114,
                  "children": []
                },
                {
                  "id": "0c4809e0-cb97-447d-9048-27bcb8e57abd",
                  "title": "Các Dạng Chính Tắc",
                  "level": 4,
                  "path": "1.1.4.7",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 781,
                  "children": []
                }
              ]
            }
          ]
        },
        {
          "id": "661d8f77-7381-41a8-8ac7-bddec66e6373",
          "title": "Vị từ",
          "level": 2,
          "path": "1.2",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "8fb286cb-fb72-400a-b3bb-bd3dc9554fec",
              "title": "Khái niệm vị từ",
              "level": 3,
              "path": "1.2.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 585,
              "children": []
            },
            {
              "id": "81853029-fcca-4000-9e64-e2cd36867480",
              "title": "Các phép toán trên vị từ",
              "level": 3,
              "path": "1.2.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 330,
              "children": []
            },
            {
              "id": "c43cecc7-252d-4ff3-9135-2def36f07c2e",
              "title": "Một số qui tắc suy luận",
              "level": 3,
              "path": "1.2.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 0,
              "children": [
                {
                  "id": "0bc6aec0-063e-4709-85e6-485957ee7914",
                  "title": "Qui tắc phủ định ( DeMorgan).",
                  "level": 4,
                  "path": "1.2.3.1",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 36,
                  "children": []
                },
                {
                  "id": "81874a4f-5beb-4c97-b02e-366d76897069",
                  "title": "Qui tắc thay đổi thứ tự lượng từ hoá 2 biến.",
                  "level": 4,
                  "path": "1.2.3.2",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 78,
                  "children": []
                },
                {
                  "id": "c72b56cb-bf79-4e24-9f8c-b8dad435d655",
                  "title": "Qui tắc kéo theo.",
                  "level": 4,
                  "path": "1.2.3.3",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 16,
                  "children": []
                },
                {
                  "id": "6f4ffb2e-f147-47f5-adff-c259e8614653",
                  "title": "Qui tắc đặc biệt hoá phổ dụng.",
                  "level": 4,
                  "path": "1.2.3.4",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 59,
                  "children": []
                },
                {
                  "id": "1f87bbdd-623b-4da4-8271-223ff9fd5885",
                  "title": "Qui tắc tổng quát hoá phổ dụng.",
                  "level": 4,
                  "path": "1.2.3.5",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 83,
                  "children": []
                }
              ]
            },
            {
              "id": "f85ff217-f637-49b8-bc76-c2c151356bb4",
              "title": "Các ví dụ",
              "level": 3,
              "path": "1.2.4",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1954,
              "children": []
            },
            {
              "id": "5f3f9ff8-7a0c-47db-b03f-75cfecbc6641",
              "title": "Lượng từ",
              "level": 3,
              "path": "1.2.5",
              "page_start": null,
              "page_end": null,
              "text_char_count": 0,
              "children": [
                {
                  "id": "7d3f363b-9218-4f69-ba3c-c0bc1f3a4496",
                  "title": "Ví dụ:",
                  "level": 4,
                  "path": "1.2.5.1",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 199,
                  "children": []
                },
                {
                  "id": "8d84a071-f975-4c0e-8cf3-200c107aa367",
                  "title": "Khái niệm lượng từ",
                  "level": 4,
                  "path": "1.2.5.2",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 560,
                  "children": []
                }
              ]
            }
          ]
        },
        {
          "id": "a392c6cc-a8b7-4f70-b5bb-639e077132cb",
          "title": "Suy luận toán học",
          "level": 2,
          "path": "1.3",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "b3aef5dd-effc-4a5c-831a-c250769d8d7c",
              "title": "Khái niệm",
              "level": 3,
              "path": "1.3.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 581,
              "children": []
            },
            {
              "id": "6c5b4cc3-404d-4661-913b-c0f58c8a1bfb",
              "title": "Các phương pháp kiểm tra một luật suy diễn.",
              "level": 3,
              "path": "1.3.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 163,
              "children": []
            },
            {
              "id": "c7ae1ba0-5370-4565-af76-76544ea44b0e",
              "title": "Các qui tắc suy diễn cơ bản",
              "level": 3,
              "path": "1.3.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 315,
              "children": []
            }
          ]
        },
        {
          "id": "5b5d1e9d-4266-4644-9b3a-637aaeea83ec",
          "title": "Các phương pháp chứng minh",
          "level": 2,
          "path": "1.4",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "428e92e3-2ed1-4b0f-92b0-858dcc999076",
              "title": "Một số ví dụ.",
              "level": 3,
              "path": "1.4.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 0,
              "children": [
                {
                  "id": "57e40632-c622-436c-a6a5-9f3550b8d960",
                  "title": "Khái niệm:",
                  "level": 4,
                  "path": "1.4.1.1",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 215,
                  "children": []
                },
                {
                  "id": "7588af35-e67d-4e42-846e-6b2d1c9b2531",
                  "title": "Các ví dụ",
                  "level": 4,
                  "path": "1.4.1.2",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 2294,
                  "children": []
                },
                {
                  "id": "587613a9-5f37-4f71-84a7-865b9e6a07e2",
                  "title": "Nguyên lý qui nạp",
                  "level": 4,
                  "path": "1.4.1.3",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 3809,
                  "children": [
                    {
                      "id": "7d587343-4189-4e2c-a30b-c93f0ff20540",
                      "title": "C: \"Tôi vô tội\"",
                      "level": 6,
                      "path": "1.4.1.3.1",
                      "page_start": null,
                      "page_end": null,
                      "text_char_count": 1740,
                      "children": []
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "id": "7f6e4af7-d95e-452c-917f-faac798eb100",
      "title": "ĐẠI SỐ BOOL",
      "level": 1,
      "path": "2",
      "page_start": null,
      "page_end": null,
      "text_char_count": 0,
      "children": [
        {
          "id": "d10dcadc-bff4-4c81-9cc9-c6ccf30ac618",
          "title": "Khái niệm phép toán",
          "level": 2,
          "path": "2.1",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "f4fd3b8d-eeac-41b9-a73d-86e49ca55c1a",
              "title": "Ví dụ",
              "level": 3,
              "path": "2.1.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 74,
              "children": [
                {
                  "id": "4c72d284-a00d-43b2-9bbd-6951188bed13",
                  "title": "Cộng",
                  "level": 4,
                  "path": "2.1.1.1",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 156,
                  "children": []
                },
                {
                  "id": "f2c02982-6efb-4ad4-a41e-de55e69d628d",
                  "title": "Nhân",
                  "level": 4,
                  "path": "2.1.1.2",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 408,
                  "children": []
                }
              ]
            },
            {
              "id": "3184cce8-8f8b-4773-b32a-a047dca78544",
              "title": "Định nghĩa",
              "level": 3,
              "path": "2.1.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 240,
              "children": []
            },
            {
              "id": "15354976-368c-4f25-b56d-dd95a9a17997",
              "title": "Các khái niệm về tính chất (phép toán 2 ngôi).",
              "level": 3,
              "path": "2.1.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 683,
              "children": []
            },
            {
              "id": "089c30be-855c-44ec-8222-c01201a72cbf",
              "title": "Khái niệm đại số",
              "level": 3,
              "path": "2.1.4",
              "page_start": null,
              "page_end": null,
              "text_char_count": 93,
              "children": []
            }
          ]
        },
        {
          "id": "04b3f7fa-8437-40df-8cbb-1baf9d39e696",
          "title": "Biểu thức bool và hàm bool.",
          "level": 2,
          "path": "2.2",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "2ea10d8e-7fea-4b63-9b52-f656f1bacab8",
              "title": "Đại số Boole",
              "level": 3,
              "path": "2.2.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 0,
              "children": [
                {
                  "id": "fd56f9d8-83e6-438c-9333-5f4eeea4b2c6",
                  "title": "Một số ví dụ",
                  "level": 4,
                  "path": "2.2.1.1",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 784,
                  "children": []
                },
                {
                  "id": "dd8e1040-7f37-4197-aabb-9d897ade91be",
                  "title": "Định nghĩa",
                  "level": 4,
                  "path": "2.2.1.2",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 365,
                  "children": []
                }
              ]
            },
            {
              "id": "e1854f6c-a915-4d10-abbf-8747f1673d58",
              "title": "Các tính chất đại số Boole",
              "level": 3,
              "path": "2.2.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 536,
              "children": []
            },
            {
              "id": "2c10b44c-3381-4278-95c1-a2bbcd2a202c",
              "title": "Đẳng cấu Boole, Định lý Stone",
              "level": 3,
              "path": "2.2.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 0,
              "children": [
                {
                  "id": "665ab7d9-d2bf-4ec8-9190-05f060191493",
                  "title": "Định nghĩa đẳng cấu Boole",
                  "level": 4,
                  "path": "2.2.3.1",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 167,
                  "children": []
                },
                {
                  "id": "abf69e42-792e-4d60-89a8-036e9408be74",
                  "title": "Định lý Stone (định lý biểu diễn).",
                  "level": 4,
                  "path": "2.2.3.2",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 39,
                  "children": []
                }
              ]
            },
            {
              "id": "cacba705-a298-4fb5-a39a-071e7c490259",
              "title": "Hàm Boole.",
              "level": 3,
              "path": "2.2.4",
              "page_start": null,
              "page_end": null,
              "text_char_count": 0,
              "children": [
                {
                  "id": "0f17f20c-b947-4a06-ac26-828b360f893c",
                  "title": "Khái niệm nguyên tử.",
                  "level": 4,
                  "path": "2.2.4.1",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 405,
                  "children": []
                },
                {
                  "id": "83b6c538-447c-464e-9a47-b7f222bce413",
                  "title": ". Định nghĩa hàm Boole",
                  "level": 4,
                  "path": "2.2.4.2",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 407,
                  "children": []
                }
              ]
            },
            {
              "id": "f287de7a-f042-4992-b7e8-afca9ff380b8",
              "title": "Biểu thức Boole",
              "level": 3,
              "path": "2.2.5",
              "page_start": null,
              "page_end": null,
              "text_char_count": 0,
              "children": [
                {
                  "id": "2cde13f3-ef26-4a38-ad27-aa7357a29f6e",
                  "title": "Định nghĩa 1",
                  "level": 4,
                  "path": "2.2.5.1",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 437,
                  "children": []
                },
                {
                  "id": "9cffc231-f60f-4251-b7d0-227382f1f22c",
                  "title": "Định nghĩa 2",
                  "level": 4,
                  "path": "2.2.5.2",
                  "page_start": null,
                  "page_end": null,
                  "text_char_count": 410,
                  "children": []
                }
              ]
            },
            {
              "id": "27eeba3c-c0af-463e-9beb-730287d1c427",
              "title": "Cổng logic",
              "level": 3,
              "path": "2.2.6",
              "page_start": null,
              "page_end": null,
              "text_char_count": 311,
              "children": []
            }
          ]
        },
        {
          "id": "357e22f2-2a12-4b71-8b7c-9c8f12496eb1",
          "title": "Tối ưu hóa",
          "level": 2,
          "path": "2.3",
          "page_start": null,
          "page_end": null,
          "text_char_count": 417,
          "children": []
        },
        {
          "id": "5c379d5c-db87-4dc0-87ee-0f5230a44dc9",
          "title": "Biểu đồ Karnaugh.",
          "level": 2,
          "path": "2.4",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "b7a1041a-cb99-4751-b4e0-d47c4d85bf99",
              "title": "Biểu diễn tích cơ bản",
              "level": 3,
              "path": "2.4.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 52,
              "children": []
            },
            {
              "id": "a6f1679e-2cdd-446e-8dee-2692616affbe",
              "title": "Tính chất biểu đồ Karnaugh",
              "level": 3,
              "path": "2.4.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 67,
              "children": []
            },
            {
              "id": "792660ec-59ae-4ad7-911d-6724df4afe9b",
              "title": "Khái niệm tế bào lớn",
              "level": 3,
              "path": "2.4.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 33,
              "children": []
            },
            {
              "id": "d8c4768a-656f-4b97-b851-c519b89046ab",
              "title": "Thuật toán Karnaugh",
              "level": 3,
              "path": "2.4.4",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1903,
              "children": []
            }
          ]
        }
      ]
    },
    {
      "id": "06dc2aab-0e4b-4e70-8c8a-6f4f35ca030e",
      "title": "PHÉP ĐẾM",
      "level": 1,
      "path": "3",
      "page_start": null,
      "page_end": null,
      "text_char_count": 0,
      "children": [
        {
          "id": "0e291045-e5a3-4607-8d41-f19db6c56725",
          "title": "Giới thiệu tập hợp",
          "level": 2,
          "path": "3.1",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "4b169142-044f-4ab2-972b-c93338cc5657",
              "title": "Khái niệm tập hợp",
              "level": 3,
              "path": "3.1.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1567,
              "children": []
            },
            {
              "id": "9654b109-6319-478d-a846-d433f18a1030",
              "title": "Quan hệ bao hàm và tập con",
              "level": 3,
              "path": "3.1.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 236,
              "children": []
            },
            {
              "id": "b5354d31-9f89-4fde-b323-481e483eb284",
              "title": "Quan hệ bằng nhau",
              "level": 3,
              "path": "3.1.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 475,
              "children": []
            },
            {
              "id": "9e3b886d-be87-4929-ac9b-2a4523b616e7",
              "title": "Các phép toán trên tập hợp.",
              "level": 3,
              "path": "3.1.4",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1326,
              "children": []
            }
          ]
        },
        {
          "id": "397f84e4-bc50-489f-81d6-d85be54c7370",
          "title": "Ánh Xạ",
          "level": 2,
          "path": "3.2",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "60b5ce8e-bd9e-4091-a932-fb06100a7d08",
              "title": "Khái niệm ánh xạ",
              "level": 3,
              "path": "3.2.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 360,
              "children": []
            },
            {
              "id": "3af54eaf-e7b8-4071-977d-71efc539846c",
              "title": "Các ánh xạ đặc biệt",
              "level": 3,
              "path": "3.2.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 574,
              "children": []
            }
          ]
        },
        {
          "id": "cec72b77-9f09-4606-b910-c04659803e37",
          "title": "Số Nguyên",
          "level": 2,
          "path": "3.3",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "c7ab158b-8404-4e3f-b62d-0d84d86e70fa",
              "title": "Giới thiệu các tập hợp số",
              "level": 3,
              "path": "3.3.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 169,
              "children": []
            },
            {
              "id": "d134b278-1878-4bb4-b99c-164961c2602e",
              "title": "Phép toán số học trên tập số  nguyên",
              "level": 3,
              "path": "3.3.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 304,
              "children": []
            },
            {
              "id": "37ed7a24-0a56-418f-ad7e-ce0855316483",
              "title": "Một số tính chất của tập số nguyên",
              "level": 3,
              "path": "3.3.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 163,
              "children": []
            },
            {
              "id": "a21af2c4-98d2-4891-9017-ce575c1ae1ef",
              "title": "Phép chia trên tập số nguyên",
              "level": 3,
              "path": "3.3.4",
              "page_start": null,
              "page_end": null,
              "text_char_count": 320,
              "children": []
            },
            {
              "id": "0bde9546-c6d2-4328-8d30-2a3f0ba9957d",
              "title": "Uớc số chung lớn nhất, bội số chung nhỏ nhất",
              "level": 3,
              "path": "3.3.5",
              "page_start": null,
              "page_end": null,
              "text_char_count": 952,
              "children": []
            },
            {
              "id": "01d503a7-c1e3-40f9-ac0b-35ea9f33228b",
              "title": "Số nguyên tố",
              "level": 3,
              "path": "3.3.6",
              "page_start": null,
              "page_end": null,
              "text_char_count": 665,
              "children": []
            }
          ]
        },
        {
          "id": "5bf2942d-02aa-43d2-8bda-02a4d63d78ae",
          "title": "Nguyên Lý Đếm",
          "level": 2,
          "path": "3.4",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "1abf518b-128e-4cef-9494-a8022583c235",
              "title": "Nguyên lý nhân",
              "level": 3,
              "path": "3.4.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 3462,
              "children": []
            },
            {
              "id": "b409d56b-0acc-4c8e-b33a-c44c5322c804",
              "title": "Nguyên lý cộng",
              "level": 3,
              "path": "3.4.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1662,
              "children": []
            },
            {
              "id": "6dfd73dc-90d0-4352-830c-88e5fbc2831c",
              "title": "Nguyên lý bù trừ",
              "level": 3,
              "path": "3.4.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1987,
              "children": []
            }
          ]
        },
        {
          "id": "1378d0fb-28e1-4af4-a1fb-25d2a6bb0376",
          "title": "Nguyên lý  DIRICHLET",
          "level": 2,
          "path": "3.5",
          "page_start": null,
          "page_end": null,
          "text_char_count": 4120,
          "children": []
        },
        {
          "id": "edadec25-376a-4d78-86a0-f36059e0d5ee",
          "title": "Xác suất rời rạc",
          "level": 2,
          "path": "3.6",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "c4a87c0b-350a-424a-8fd5-34e29134cabe",
              "title": "Chỉnh hợp",
              "level": 3,
              "path": "3.6.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1253,
              "children": []
            },
            {
              "id": "bf04129b-7b37-4449-8870-4074a7025ad0",
              "title": "Hoán vị",
              "level": 3,
              "path": "3.6.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1523,
              "children": []
            },
            {
              "id": "567cb02f-15e3-443c-ad70-ea00e555297f",
              "title": "Tổ hợp",
              "level": 3,
              "path": "3.6.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 988,
              "children": []
            },
            {
              "id": "e949cd37-32f8-48da-8bf1-a6d365777c1f",
              "title": "Chỉnh hợp lặp",
              "level": 3,
              "path": "3.6.4",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1842,
              "children": []
            },
            {
              "id": "c77ca6ec-95d7-4d0e-9486-904c9bf45768",
              "title": "Tổ hợp lặp",
              "level": 3,
              "path": "3.6.5",
              "page_start": null,
              "page_end": null,
              "text_char_count": 3285,
              "children": []
            }
          ]
        }
      ]
    },
    {
      "id": "c7c77569-e889-46a5-86e8-b44af1e78f6b",
      "title": "LÝ THUYẾT CHIA",
      "level": 1,
      "path": "4",
      "page_start": null,
      "page_end": null,
      "text_char_count": 0,
      "children": [
        {
          "id": "c6e59419-9bc7-4895-b20f-ecb97b0e9bd4",
          "title": "Phép chia hết và chia có dư",
          "level": 2,
          "path": "4.1",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "d8328400-51d6-4ac2-ac08-83d5e479d436",
              "title": "Phép chia hết",
              "level": 3,
              "path": "4.1.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 563,
              "children": []
            },
            {
              "id": "123f2ae7-f156-4556-b260-173ca7c055f7",
              "title": "Phép chia có dư",
              "level": 3,
              "path": "4.1.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 166,
              "children": []
            }
          ]
        },
        {
          "id": "c10bd6fe-05cc-4145-becd-79e22d35ee1d",
          "title": "Ước chung lớn nhất và bội chung nhỏ nhất",
          "level": 2,
          "path": "4.2",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "956f9020-a62b-4ec6-b95d-1ee352367e8a",
              "title": "Ước chung lớn nhất (UCLN)",
              "level": 3,
              "path": "4.2.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 2279,
              "children": []
            },
            {
              "id": "4be9dd76-786e-42f5-8cad-46e2684e043c",
              "title": "Bội chung nhỏ nhất (BCNN)",
              "level": 3,
              "path": "4.2.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1192,
              "children": []
            }
          ]
        },
        {
          "id": "f30880a0-c2bd-41d8-9df2-e0ab6b8f1898",
          "title": "Số nguyên tố và hợp số",
          "level": 2,
          "path": "4.3",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "f1922487-8ed3-44aa-977d-ef083cb19ef1",
              "title": "Số nguyên tố",
              "level": 3,
              "path": "4.3.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 256,
              "children": []
            },
            {
              "id": "6a33f4e1-c505-40e9-ae69-c53d6d54a7d1",
              "title": "Hợp số",
              "level": 3,
              "path": "4.3.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 648,
              "children": []
            }
          ]
        },
        {
          "id": "bffa2491-29e8-4fa3-8b1a-c5a349f8fe8b",
          "title": "Bảng số nguyên tố - Sàng Erathosthene",
          "level": 2,
          "path": "4.4",
          "page_start": null,
          "page_end": null,
          "text_char_count": 884,
          "children": []
        },
        {
          "id": "f141a6cb-6fc6-4b18-9093-4e2491cf2e7d",
          "title": "Định lý cơ bản của số học",
          "level": 2,
          "path": "4.5",
          "page_start": null,
          "page_end": null,
          "text_char_count": 1611,
          "children": []
        },
        {
          "id": "f991f64b-1b1c-4408-8077-68f65f2e25e1",
          "title": "Phương trình nguyên",
          "level": 2,
          "path": "4.6",
          "page_start": null,
          "page_end": null,
          "text_char_count": 202,
          "children": [
            {
              "id": "234e0649-f905-481e-b008-8919de5ff577",
              "title": "Phương trình nguyên bậc nhất 2 ẩn",
              "level": 3,
              "path": "4.6.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1711,
              "children": []
            },
            {
              "id": "b0a03835-21b4-479e-a1bd-9bae4a955267",
              "title": "Phương trình nguyên bậc nhất nhiều ẩn",
              "level": 3,
              "path": "4.6.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1556,
              "children": []
            }
          ]
        }
      ]
    },
    {
      "id": "9129e4c1-4c3a-46b3-8e62-a1dabd5a3ae4",
      "title": "LÝ THUYẾT ĐỒNG DƯ",
      "level": 1,
      "path": "5",
      "page_start": null,
      "page_end": null,
      "text_char_count": 0,
      "children": [
        {
          "id": "4a24324b-e329-4264-9807-3a0f4e176478",
          "title": "Quan hệ đồng dư",
          "level": 2,
          "path": "5.1",
          "page_start": null,
          "page_end": null,
          "text_char_count": 1506,
          "children": []
        },
        {
          "id": "47d42866-55d0-495f-afa8-4389bc53d380",
          "title": "Phương trình đồng dư một ẩn",
          "level": 2,
          "path": "5.2",
          "page_start": null,
          "page_end": null,
          "text_char_count": 0,
          "children": [
            {
              "id": "91b93cd3-7ea1-4847-8e76-e644999b19dd",
              "title": "Phương trình đồng dư một ẩn",
              "level": 3,
              "path": "5.2.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 2163,
              "children": []
            },
            {
              "id": "002c5a7a-0a99-4720-9c8b-acffe53f6049",
              "title": "Phương trình đồng dư bậc nhất một ẩn",
              "level": 3,
              "path": "5.2.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 927,
              "children": []
            }
          ]
        },
        {
          "id": "863d51bb-9d20-4539-a824-50fbf8d6e769",
          "title": "Hệ phương trình đồng dư bậc nhất một ẩn",
          "level": 2,
          "path": "5.3",
          "page_start": null,
          "page_end": null,
          "text_char_count": 2554,
          "children": []
        },
        {
          "id": "2b223474-ae11-41e2-bff0-b687e22b95f8",
          "title": "Hệ phương trình đồng dư bậc cao một ẩn",
          "level": 2,
          "path": "5.4",
          "page_start": null,
          "page_end": null,
          "text_char_count": 1996,
          "children": []
        },
        {
          "id": "2974eed7-bf71-4d62-81c0-b4bd0363d318",
          "title": "Ứng dụng của lý thuyết đồng dư",
          "level": 2,
          "path": "5.5",
          "page_start": null,
          "page_end": null,
          "text_char_count": 169,
          "children": [
            {
              "id": "6d5e6ed2-8bc6-4f1a-a265-9cb9f5a5adb7",
              "title": "Các hàm băm",
              "level": 3,
              "path": "5.5.1",
              "page_start": null,
              "page_end": null,
              "text_char_count": 1105,
              "children": []
            },
            {
              "id": "f805cf7d-6f6d-4166-9ab1-667034c1b623",
              "title": "Các số giả ngẫu nhiên",
              "level": 3,
              "path": "5.5.2",
              "page_start": null,
              "page_end": null,
              "text_char_count": 876,
              "children": []
            },
            {
              "id": "162f2baf-3bd9-4e8e-b738-270cfebde05e",
              "title": "Mật mã",
              "level": 3,
              "path": "5.5.3",
              "page_start": null,
              "page_end": null,
              "text_char_count": 2142,
              "children": []
            }
          ]
        }
      ]
    }
  ]
}
```

///////////////////// /api/v1/books/{book_id}/learning-units

```json
{
  "book_id": "5ef640e3-40f5-4fa6-8343-b6fd6a03c305",
  "mode": "pareto",
  "total_units": 4,
  "units": [
    {
      "id": "6e7f8eea-29b5-4447-83ec-3aec02096e58",
      "title": "LOGIC MỆNH ĐỀ - Phần 1/2",
      "status": "ready",
      "unit_index": 0,
      "unit_type": "pareto_focus",
      "source_text_char_count": 14147,
      "estimated_audio_seconds": 1515,
      "main_segment_count": 6,
      "review_text": "Trong phần này, chúng ta đã tìm hiểu về mệnh đề toán học, định nghĩa là phát biểu có chân trị đúng hoặc sai. Mệnh đề có thể là sơ cấp hoặc phức hợp, được phân tích bằng bảng chân trị. Các phép toán logic cơ bản gồm phủ định, và, hoặc, kéo theo, và tương đương, mỗi phép có quy tắc chân trị riêng. Biểu thức logic được xây dựng từ các mệnh đề và phép toán, và hai biểu thức được coi là tương đương logic nếu chúng có cùng chân trị. Chúng ta cũng đã khám phá vị từ, là hàm biến thành mệnh đề khi gán giá trị, và các lượng từ phổ dụng, tồn tại. Cuối cùng, suy luận logic và chứng minh là quá trình xác định tính đúng đắn của các khẳng định dựa trên các luật và quy tắc suy diễn như Modus Ponens và Modus Tollens.",
      "review_audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_1/pareto/review.mp3",
      "planner_reason": "Tách từ nhóm lớn thành phần 1/2 để không vượt giới hạn xử lý.",
      "segments": []
    },
    {
      "id": "056ebc7c-936d-4bd7-af6c-7c1062abaec2",
      "title": "LOGIC MỆNH ĐỀ - Phần 2/2",
      "status": "ready",
      "unit_index": 1,
      "unit_type": "pareto_focus",
      "source_text_char_count": 7847,
      "estimated_audio_seconds": 790,
      "main_segment_count": 11,
      "review_text": "Trong phần này, chúng ta đã tìm hiểu về các mô hình suy diễn trong logic, phân biệt giữa suy diễn đúng và sai qua các ví dụ cụ thể. Chúng ta cũng khám phá các phương pháp chứng minh quan trọng như phản chứng và chứng minh theo trường hợp. Đặc biệt, nguyên lý quy nạp được giới thiệu chi tiết với hai dạng: quy nạp yếu và quy nạp mạnh, cùng các bước cơ sở và quy nạp. Các ví dụ áp dụng quy nạp đã minh họa cách chứng minh các công thức tổng, tính chia hết, và các tính chất toán học khác. Điểm mấu chốt là hiểu rõ cách xây dựng một lập luận logic và các kỹ thuật chứng minh cơ bản.",
      "review_audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_2/pareto/review.mp3",
      "planner_reason": "Tách từ nhóm lớn thành phần 2/2 để không vượt giới hạn xử lý.",
      "segments": []
    },
    {
      "id": "bbbbeab0-6d43-4a69-9836-6f8ebe8275a7",
      "title": "PHÉP ĐẾM - Phần 1/2",
      "status": "ready",
      "unit_index": 2,
      "unit_type": "pareto_focus",
      "source_text_char_count": 14250,
      "estimated_audio_seconds": 1592,
      "main_segment_count": 22,
      "review_text": "Trong phần này, chúng ta đã tìm hiểu về các khái niệm cơ bản của tập hợp, bao gồm định nghĩa, cách biểu diễn, các quan hệ như tập con và tập bằng nhau. Chúng ta cũng đã nắm vững các phép toán trên tập hợp như hợp, giao, hiệu, và phần bù, cùng với các tính chất quan trọng của chúng. Tiếp theo, chúng ta khám phá khái niệm ánh xạ, các loại ánh xạ như đơn ánh, toàn ánh, song ánh, và các phép toán trên ánh xạ. Phần cuối cùng tập trung vào các tập số cơ bản, phép chia hết, ước số chung lớn nhất, bội số chung nhỏ nhất, số nguyên tố và các định lý liên quan. Cuối cùng, chúng ta đã học ba nguyên lý đếm cốt lõi: nguyên lý nhân, nguyên lý cộng và nguyên lý bù trừ, cùng với các ứng dụng của chúng trong việc giải quyết các bài toán đếm.",
      "review_audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_3/pareto/review.mp3",
      "planner_reason": "Tách từ nhóm lớn thành phần 1/2 để không vượt giới hạn xử lý.",
      "segments": []
    },
    {
      "id": "2837a054-6d57-4533-91f5-6f3850f2aada",
      "title": "PHÉP ĐẾM - Phần 2/2",
      "status": "ready",
      "unit_index": 3,
      "unit_type": "pareto_focus",
      "source_text_char_count": 13021,
      "estimated_audio_seconds": 1392,
      "main_segment_count": 16,
      "review_text": "Trong phần này, chúng ta đã tìm hiểu về các nguyên lý đếm cơ bản. Đầu tiên là Nguyên lý Dirichlet, với hai dạng: cơ bản và tổng quát, giúp xác định sự tồn tại của ít nhất một phần tử thỏa mãn điều kiện khi phân bổ. Tiếp theo, chúng ta khám phá Chỉnh hợp, Hoán vị và Tổ hợp, phân biệt chúng dựa trên yếu tố thứ tự và sự khác biệt của các phần tử được chọn. Cuối cùng, chúng ta tìm hiểu về Chỉnh hợp lặp và Tổ hợp lặp, cho phép các phần tử được chọn có thể giống nhau. Nắm vững các định nghĩa và công thức này là chìa khóa để giải quyết các bài toán đếm trong nhiều lĩnh vực.",
      "review_audio_url": "https://sdueaskgfuelfydrgdhx.supabase.co/storage/v1/object/public/audios/5ef640e3-40f5-4fa6-8343-b6fd6a03c305/unit_4/pareto/review.mp3",
      "planner_reason": "Tách từ nhóm lớn thành phần 2/2 để không vượt giới hạn xử lý.",
      "segments": []
    }
  ]
}
```

///////////////////// /api/v1/books/{book_id}/learning-progress

```json
{
  "book_id": "5ef640e3-40f5-4fa6-8343-b6fd6a03c305",
  "mode": "pareto",
  "book_progress_percent": 0,
  "completed_units": 0,
  "playable_units": 4,
  "last_learning_unit_id": null,
  "last_segment_id": null,
  "last_segment_index": null,
  "position_ms": null,
  "units": [
    {
      "learning_unit_id": "6e7f8eea-29b5-4447-83ec-3aec02096e58",
      "mode": "pareto",
      "segment_id": null,
      "segment_index": 0,
      "position_ms": 0,
      "progress_percent": 0,
      "max_progress_percent": 0,
      "status": "not_started",
      "started_at": null,
      "last_activity_at": null,
      "completed_at": null
    },
    {
      "learning_unit_id": "056ebc7c-936d-4bd7-af6c-7c1062abaec2",
      "mode": "pareto",
      "segment_id": null,
      "segment_index": 0,
      "position_ms": 0,
      "progress_percent": 0,
      "max_progress_percent": 0,
      "status": "not_started",
      "started_at": null,
      "last_activity_at": null,
      "completed_at": null
    },
    {
      "learning_unit_id": "bbbbeab0-6d43-4a69-9836-6f8ebe8275a7",
      "mode": "pareto",
      "segment_id": null,
      "segment_index": 0,
      "position_ms": 0,
      "progress_percent": 0,
      "max_progress_percent": 0,
      "status": "not_started",
      "started_at": null,
      "last_activity_at": null,
      "completed_at": null
    },
    {
      "learning_unit_id": "2837a054-6d57-4533-91f5-6f3850f2aada",
      "mode": "pareto",
      "segment_id": null,
      "segment_index": 0,
      "position_ms": 0,
      "progress_percent": 0,
      "max_progress_percent": 0,
      "status": "not_started",
      "started_at": null,
      "last_activity_at": null,
      "completed_at": null
    }
  ]
}
```
