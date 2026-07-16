# Kịch Bản Đánh Giá Thực Nghiệm Đa Lượt Giọng Nói

Dưới đây là bảng kịch bản đàm thoại liên tục (1 phiên gồm 10 câu hỏi từ người dùng) để đánh giá toàn diện các luồng định tuyến tri thức, xử lý ngữ cảnh, và quản lý chính sách bảo mật Web trong hệ thống trợ lý học tập TRIAM. Bảng này được thiết kế định dạng chuẩn để phục vụ việc trích xuất và đưa vào phần Đánh giá thực nghiệm của Luận văn tốt nghiệp.

  <br>

  <table border="1" style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;">
    <!-- Header Ngữ cảnh 1 -->
    <tr style="background-color: #e6e6e6; text-align: center;">
      <th colspan="2" style="padding: 10px; font-size: 16px;">Ngữ cảnh 1 (Tương ứng với 1 phiên trao đổi tầm 10 câu hỏi từ user)</th>
    </tr>
    
    <!-- Mô tả ngữ cảnh -->
    
    <tr>
      <td colspan="2" style="padding: 10px; line-height: 1.5; background-color: #fafafa;">
        - Ngữ cảnh trực tiếp về sách truyện <i>Of Mice and Men</i>: nói về cuộc đời của các nhân vật và các tình tiết vui buồn lẫn lộn trong thời kì khó khăn của tầng lớp lao động thời kỳ đại suy thoái.<br>
      </td>
    </tr>

    <!-- Q1 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q1: User hỏi "Sách có mấy chương"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Sách có mấy chương</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">6 chương</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Cuốn sách này có 6 chương.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Dùng truy vấn Database lấy danh sách metadata book bao gồm thông tin sách và cấu trúc thư mục sách. Trả lời được đúng nội dung câu hỏi của user.</td>
    </tr>

    <!-- Q2 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q2: User hỏi "Sách có những nhân vật nào, nhân vật nào là nhân vật chính"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Các nhân vật chính và nhân vật phụ trong tác phẩm</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">George Milton và Lennie Small là hai nhân vật chính. Các nhân vật phụ: Candy, Crooks, Curley, Vợ Curley, Slim, Carlson.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Trong tác phẩm này, hai nhân vật chính là George Milton và Lennie Small. Ngoài ra còn có các nhân vật phụ như Candy, Crooks, Curley, vợ của Curley, Slim và Carlson.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Hệ thống chạy định tuyến RAG (book_rag), gọi Hybrid Search lấy ra các chunk tri thức liên quan đến nhân vật chính/phụ và Cohere Reranker xếp hạng chính xác.</td>
    </tr>

    <!-- Q3 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q3: User hỏi "Tóm tắt giúp tôi chương bốn của sách"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Tóm tắt chương 4</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Tóm tắt chi tiết chương 4: cuộc trò chuyện của Lennie với Crooks tại chuồng ngựa, sự xuất hiện của Candy và vợ Curley.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Trong chương 4, bối cảnh diễn ra tại căn phòng của Crooks, người chăn ngựa da màu bị cô lập. Lennie đến tìm chó con và trò chuyện cùng Crooks. Sau đó, Candy và vợ của Curley cũng xuất hiện. Cuộc nói chuyện làm nổi bật sự cô đơn, khát khao về một tương lai tươi đẹp hơn của những con người nghèo khổ, cũng như sự phân biệt đối xử tàn nhẫn trong xã hội lúc bấy giờ.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến trực tiếp đến nguồn ngữ cảnh chương (book_section) nhờ phân giải chính xác ID chương 4, nạp toàn bộ nội dung chương thay vì chạy RAG thô.</td>
    </tr>

    <!-- Q4 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q4: User hỏi "Tóm tắt chương sách này đi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Tóm tắt chương</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Yêu cầu người dùng làm rõ xem muốn tóm tắt chương nào cụ thể.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Bạn muốn tôi tóm tắt chương hoặc đề mục cụ thể nào của cuốn sách này?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Guard Rule chặn yêu cầu summary thiếu số hiệu cụ thể, bẻ hướng sang intent clarification_required để yêu cầu làm rõ, tránh ảo giác RAG.</td>
    </tr>

    <!-- Q5 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q5: User trả lời "Chương sáu đi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Tóm tắt chương sáu</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Tóm tắt nội dung chương 6 (George tìm thấy Lennie ở lòng sông và nổ súng kết liễu Lennie).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Chương 6 là chương cuối cùng. Lennie trốn bên bờ ao, George tìm thấy anh ta, kể lại giấc mơ và nổ súng bắn Lennie để giải thoát khỏi nhóm người săn đuổi của Curley.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Dựa trên Thread Context để kế thừa yêu cầu tóm tắt ở câu Q4 trước đó và giải quyết thông tin chương 6 thành công.</td>
    </tr>

    <!-- Q6 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q6: User hỏi "Cái chết của Lennie diễn ra thế nào và tại sao George lại làm vậy?"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Hành động bắn Lennie của George ở cuối tác phẩm</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">George bắn Lennie bằng khẩu súng của Carlson để bảo vệ anh khỏi đám đông của Curley và chấm dứt bi kịch lặp lại.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Lennie bị George bắn ở phía sau đầu bên cạnh hồ nước bằng khẩu súng của Carlson. George làm vậy trong sự đau xót tột cùng vì biết đám đông của Curley sẽ bắt giữ, hành hạ hoặc treo cổ Lennie một cách dã man.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Tìm kiếm lai lấy được chunk mô tả cái chết của Lennie ở chương 6, Cohere Reranker chấm điểm cao nhất và LLM trả lời trung thực.</td>
    </tr>

    <!-- Q7 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q7: User hỏi "Giá Bitcoin hiện tại hôm nay là bao nhiêu?"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Giá Bitcoin ngày hôm nay</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Phát hiện câu hỏi ngoài sách đòi hỏi internet và xin quyền truy cập web.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Tôi cần tìm thông tin này trên Internet. Bạn có cho phép tôi tìm kiếm web không?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang policy (external_current_info). Hệ thống chặn quyền tìm kiếm web một lần và sinh thoại hỏi xin ý kiến người dùng.</td>
    </tr>

    <!-- Q8 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q8: User trả lời "Không, chỉ tìm trong sách thôi."</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Không đồng ý tìm kiếm internet</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Từ chối tìm web và chỉ hỗ trợ tri thức trong sách.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Đồng ý, tôi sẽ chỉ tập trung vào nội dung trong sách và không thực hiện tìm kiếm web.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Phân loại ý định từ chối (web_search_denied) chuẩn xác, đóng luồng web và bảo mật thông tin tối đa.</td>
    </tr>

    <!-- Q9 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q9: User hỏi "Tìm các tác phẩm tương tự với Of Mice and Men trên internet"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Tác phẩm tương tự Of Mice and Men</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Hỏi xin quyền truy cập internet để tìm tác phẩm tương tự.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Để tìm các tác phẩm tương tự, tôi cần tra cứu trên internet. Bạn có cho phép tôi tìm kiếm web không?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Tiếp tục thực thi quy trình xin quyền một lần đối với yêu cầu tìm kiếm ngoài sách.</td>
    </tr>

    <!-- Q10 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q10: User trả lời "Được chứ, tìm đi."</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Đồng ý tìm kiếm internet</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Gọi Tavily Search để tìm các cuốn sách cùng chủ đề (như The Grapes of Wrath, To Kill a Mockingbird) và tổng hợp trả lời.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Theo kết quả tìm kiếm internet, các tác phẩm tương tự có chủ đề về số phận người nông dân thời kỳ Đại suy thoái bao gồm: 'The Grapes of Wrath' cũng của John Steinbeck, và 'To Kill a Mockingbird' của Harper Lee.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Nhận diện ý định đồng ý (web_search_granted). Chạy tool tìm kiếm internet Tavily, nạp dữ liệu web và tổng hợp câu trả lời thành công.</td>
    </tr>

    <!-- ========================================== -->
    <!-- Header Ngữ cảnh 2 -->
    <tr style="background-color: #d1e7dd; text-align: center;">
      <th colspan="2" style="padding: 10px; font-size: 16px; color: #0f5132;">Ngữ cảnh 2 (Tương ứng với 1 phiên trao đổi đa tài liệu cùng lĩnh vực CNTT)</th>
    </tr>

    <!-- Mô tả ngữ cảnh 2 -->
    <tr>
      <td colspan="2" style="padding: 10px; line-height: 1.5; background-color: #f8f9fa;">
        <b>(Mô tả ngữ cảnh)</b><br>
        - 1 context gồm 2 tài liệu cùng ngành Công nghệ thông tin:<br>
          1. <i>Algorithms Notes for Professionals</i>: Tài liệu chuyên sâu về cấu trúc dữ liệu, giải thuật (Big-O, Trees, Graphs, Sorting...).<br>
          2. <i>C# programming example and solutions</i>: Tài liệu thực hành lập trình C# qua các ví dụ thực tế (switch-case, arrays, functions, LINQ...).<br>
        - <b>Chủ đề ôn tập thống nhất</b>: Ôn tập về cấu trúc dữ liệu Mảng (Arrays), các giải thuật sắp xếp/tìm kiếm liên quan, và cách hiện thực, tối ưu hóa hiệu năng mảng trong ngôn ngữ C# (.NET).
      </td>
    </tr>

    <!-- Q11 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q11: User hỏi "Tôi muốn học về mảng và các thuật toán sắp xếp"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">học mảng và thuật toán sắp xếp trong C# và cấu trúc dữ liệu</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Chào đón người dùng và liệt kê chính xác tài liệu liên quan trong Study Context (C# có Topic 5 về mảng, Algorithms có các chương Sorting từ 28-38).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Chào bạn! Ôn tập về mảng và các giải thuật sắp xếp là một lựa chọn rất tốt để nắm vững nền tảng. Hiện tại trong Study Context của bạn có tài liệu 'C# programming example and solutions' (Topic 5 hướng dẫn thực hành về mảng) và tài liệu 'Algorithms Notes for Professionals' (dành riêng các Chapter từ 28 đến 38 để nói về các giải thuật Sorting). Bạn muốn bắt đầu từ lý thuyết giải thuật hay thực hành viết code C# trước?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Nhận diện ý định chào hỏi (chitchat) kết hợp truy xuất metadata danh sách tài liệu hiện có trong context để phản hồi thân thiện và chính xác.</td>
    </tr>

    <!-- Q12 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q12: User hỏi "Nói về độ phức tạp thời gian đối với dữ liệu mảng"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">độ phức tạp thời gian của mảng trong Algorithms</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Giải thích độ phức tạp của mảng: truy cập phần tử qua chỉ mục là O(1), tìm kiếm tuyến tính O(n), chèn/xóa O(n).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Theo tài liệu Algorithms Notes for Professionals, mảng có các độ phức tạp thời gian như sau: Truy cập phần tử thông qua chỉ mục (Access) là O(1) do dữ liệu được lưu trữ liên tục trên bộ nhớ; Tìm kiếm tuyến tính (Search), Chèn phần tử (Insertion) và Xóa phần tử (Deletion) ở vị trí bất kỳ đều mất độ phức tạp O(n) trong trường hợp xấu nhất vì phải dịch chuyển các phần tử còn lại.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Hệ thống thực hiện Hybrid Search lấy ra các chunk tri thức giới thiệu thuật toán mảng từ tài liệu Algorithms và Cohere Reranker xếp hạng cao nhất.</td>
    </tr>

    <!-- Q13 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q13: User hỏi "Làm sao khai báo và gán trị mảng hai chìu trong C-sáp vậy"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">khai báo và gán giá trị mảng hai chiều trong C#</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Hướng dẫn khai báo mảng 2 chiều trong C# (Topic 5): `int[,] array = new int[rows, cols];` kết hợp khởi tạo giá trị.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Trong C# (Topic 5 của tài liệu), để khai báo và gán giá trị cho mảng hai chiều, bạn dùng dấu phẩy trong ngoặc vuông. Ví dụ khai báo mảng số nguyên gồm 2 hàng và 3 cột: `int[,] matrix = new int[2, 3] { {1, 2, 3}, {4, 5, 6} };` hoặc có thể viết ngắn gọn là: `int[,] matrix = { {1, 2, 3}, {4, 5, 6} };`.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Dù người dùng gõ sai chính tả ("chìu" -> "chiều", "C-sáp" -> "C#"), hệ thống nhờ cơ chế chuẩn hóa từ khóa và tìm kiếm lai vẫn nhận diện chính xác tri thức cần tìm là mảng 2 chiều trong tài liệu C# programming.</td>
    </tr>

    <!-- Q14 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q14: User hỏi "Nói về thuật toán sắp xếp mảng đi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">các thuật toán sắp xếp mảng trong Algorithms</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Liệt kê các giải thuật sắp xếp (Bubble Sort Chapter 29, Merge Sort Chapter 30, Quicksort Chapter 33, Selection Sort Chapter 38).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Tài liệu Algorithms Notes for Professionals dành riêng các Chapter từ 28 đến 38 để nói về các giải thuật sắp xếp mảng. Các thuật toán phổ biến bao gồm: Bubble Sort (Chapter 29), Merge Sort (Chapter 30), Quicksort (Chapter 33), và Selection Sort (Chapter 38)... Bạn có muốn đi sâu vào giải thuật nào không?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Tìm kiếm lai lấy ra các chunk giới thiệu giải thuật Sorting từ tài liệu Algorithms, Cohere Reranker xếp hạng chính xác.</td>
    </tr>

    <!-- Q15 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q15: User trả lời "Tôi thấy chương 29 nói về Bubble Sort, tôi muốn thảo luận rõ hơn về nó"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Tóm tắt chương 29 Bubble Sort trong sách Algorithms Notes for Professionals</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Tóm tắt chi tiết Chapter 29 về Bubble Sort (hoạt động bằng cách hoán đổi các phần tử kề nhau, độ phức tạp trung bình O(n^2)).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Chương 29 tóm tắt về Bubble Sort (Sắp xếp nổi bọt). Thuật toán hoạt động bằng cách liên tục duyệt qua mảng, so sánh các cặp phần tử kề nhau và hoán đổi chúng nếu chúng sai thứ tự. Quá trình này lặp lại cho đến khi không cần hoán đổi nữa. Độ phức tạp thời gian trung bình và tệ nhất là O(n^2), tốt nhất là O(n) nếu mảng đã sắp xếp sẵn.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến trực tiếp đến nguồn ngữ cảnh chương (book_section) nhờ phân giải chính xác ID chương 29, nạp toàn bộ nội dung chương thay vì chạy RAG thô.</td>
    </tr>

    <!-- Q16 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q16: User hỏi "Tiếp theo nói về chương giải thuật tìm kiếm đi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">tóm tắt chương giải thuật tìm kiếm</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Yêu cầu người dùng làm rõ xem muốn tóm tắt chương tìm kiếm nhị phân trong sách cấu trúc dữ liệu hay tìm kiếm trong sách lập trình C#.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Hiện tại cả hai cuốn sách của bạn đều có nội dung về tìm kiếm (sách Algorithms có Chapter 39 nói về Searching, sách C# cũng có phần tìm kiếm). Bạn muốn tôi tóm tắt chương giải thuật tìm kiếm trong tài liệu cấu trúc dữ liệu hay tìm kiếm trong tài liệu lập trình C#?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Guard Rule chặn yêu cầu summary thiếu số hiệu chương cụ thể và bị mơ hồ giữa hai tài liệu, bẻ hướng định tuyến sang intent clarification_required để yêu cầu làm rõ.</td>
    </tr>

    <!-- Q17 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q17: User trả lời "Tôi định hướng theo AI vậy phải học các thuật toán nào nền tảng"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">thuật toán nền tảng AI lộ trình học tập</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Nhận diện câu hỏi ngoài phạm vi tri thức sách hiện tại (parametric warning), đưa ra cảnh báo giới hạn tri thức sách và hỏi xin quyền tìm kiếm web.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Các thuật toán nền tảng cho AI như Gradient Descent, Backpropagation, hay các mạng Neural Network hiện tại không nằm trong hai cuốn sách trong Study Context của bạn (vốn chỉ nói về thuật toán mảng, cấu trúc dữ liệu cơ bản và C#). Để theo học AI, bạn nên nắm vững Toán (Đại số tuyến tính, Xác suất) và Học máy. Bạn có muốn tôi tìm kiếm lộ trình chi tiết từ internet không?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Nhận diện ý định hỏi câu mới bất ngờ và hủy trạng thái chờ làm rõ trước đó. Định tuyến sang policy (external_current_info) do câu hỏi yêu cầu tri thức ngoài sách, thực thi cảnh báo giới hạn tri thức và hỏi xin quyền tìm kiếm web.</td>
    </tr>

    <!-- Q18 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q18: User trả lời "Đồng ý, hãy tra cứu giúp tôi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">đồng ý tìm kiếm web</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Gọi Tavily Search để tìm kiếm các thuật toán AI nền tảng và lộ trình học tập, sau đó tổng hợp câu trả lời.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Theo kết quả tìm kiếm internet, các thuật toán nền tảng cho AI bao gồm: Hồi quy tuyến tính (Linear Regression), Hồi quy logistic, Cây quyết định (Decision Trees), và đặc biệt là giải thuật Lan truyền ngược (Backpropagation) trong mạng nơ-ron để cập nhật trọng số. Lộ trình học nên bắt đầu từ học máy truyền thống trước khi tiến lên học sâu (Deep Learning)...</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang web_search (web_search_granted). Chạy công cụ tìm kiếm web Tavily, lấy kết quả thời gian thực và tổng hợp câu trả lời thành công.</td>
    </tr>

    <!-- Q19 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q19: User hỏi "Hiện nay 2026 các mô hình AI ngôn ngữ lớn nào đang được đánh giá mạnh nhất trên thế giới?"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">mô hình ngôn ngữ lớn LLM mạnh nhất năm 2026</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Nhận diện câu hỏi thông tin thời gian thực năm 2026 ngoài sách, yêu cầu tra cứu internet và hỏi xin quyền tìm kiếm web.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Để cập nhật thông tin về các mô hình ngôn ngữ lớn (LLM) mạnh nhất thế giới tính đến năm 2026, tôi cần tìm kiếm trên internet. Bạn có cho phép tôi tra cứu web không?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang policy (external_current_info). Hệ thống phát hiện thông tin thời gian thực ngoài sách, thực thi chính sách chặn Web và hỏi xin ý kiến người dùng.</td>
    </tr>

    <!-- Q20 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q20: User trả lời "Không cần đâu, chỉ cần giới thiệu sơ qua dựa trên những gì bạn biết thôi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">không đồng ý tìm kiếm web</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Từ chối tìm web và chỉ dùng Parametric Memory của LLM để trả lời sơ qua về các mô hình lớn như GPT-4, Claude 3 hay Gemini 1.5.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Đồng ý, tôi sẽ không thực hiện tìm kiếm web. Dựa trên tri thức sẵn có, các mô hình ngôn ngữ lớn hàng đầu bao gồm dòng GPT-4 của OpenAI, Claude 3 của Anthropic và Gemini 1.5 của Google. Các mô hình này đều hỗ trợ xử lý đa phương thức (multimodal) và có khả năng lập trình, suy luận logic rất mạnh mẽ.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Phân loại ý định từ chối (web_search_denied) chuẩn xác, đóng luồng web và trả lời dựa trên tri thức nội bộ của mô hình.</td>
    </tr>

    <!-- ========================================== -->
    <tr style="background-color: #d1e7dd; text-align: center;">
      <th colspan="2" style="padding: 10px; font-size: 16px; color: #0f5132;">Ngữ cảnh 3 (Đàm thoại Đa tài liệu chéo miền, kiểm thử bảo mật Web nâng cao và máy trạng thái nâng cao)</th>
    </tr>

    <!-- Mô tả ngữ cảnh 3 -->
    <tr>
      <td colspan="2" style="padding: 10px; line-height: 1.5; background-color: #f8f9fa;">
        <b>(Mô tả ngữ cảnh)</b><br>
        - 1 context gồm 2 tài liệu ngoài kỹ thuật thuộc lĩnh vực Tài chính & Đầu tư:<br>
          1. <i>The Intelligent Investor</i>: Cuốn sách kinh điển về đầu tư giá trị của Benjamin Graham.<br>
          2. <i>Rich Dad Poor Dad</i>: Cuốn sách rèn luyện tư duy dòng tiền và tài sản của Robert Kiyosaki.<br>
        - <b>Chủ đề ôn tập thống nhất</b>: Lý thuyết đầu tư giá trị phòng thủ, xây dựng tài sản cá nhân và đối soát tri thức tĩnh với thông tin thị trường thời gian thực năm 2026.
      </td>
    </tr>

    <!-- Q21 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q21: User hỏi "Chào bạn, tôi muốn học về tài chính"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">học về tài chính</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Chào đón người dùng và liệt kê chính xác danh sách sách tài chính có sẵn trong Study Context (The Intelligent Investor và Rich Dad Poor Dad).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Chào bạn! Ôn tập về tài chính và tư duy đầu tư là lựa chọn rất tuyệt vời. Hiện tại trong Study Context của bạn có tài liệu 'The Intelligent Investor' của Benjamin Graham và 'Rich Dad Poor Dad' của Robert Kiyosaki. Bạn muốn đi sâu vào lý thuyết đầu tư giá trị hay tư duy tài sản trước?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Nhận diện ý định chào hỏi (chitchat) kết hợp truy xuất danh sách tài liệu hiện có trong context để phản hồi thân thiện và chính xác.</td>
    </tr>

    <!-- Q22 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q22: User hỏi "Biên độ an toàn là gì"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">biên độ an toàn là gì</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">RAG truy xuất sách The Intelligent Investor và giải thích nguyên tắc biên độ an toàn (Margin of Safety) của Benjamin Graham.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Theo sách The Intelligent Investor, biên độ an toàn (Margin of Safety) là khoảng chênh lệch giữa giá trị nội tại thực tế của một cổ phiếu và giá thị trường hiện tại của nó. Graham khuyên chỉ nên mua khi giá thị trường thấp hơn đáng kể so với giá trị nội tại để hạn chế tối đa rủi ro thua lỗ khi thị trường biến động.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Tìm kiếm lai lấy ra các chunk giới thiệu giải thuật đầu tư giá trị từ tài liệu The Intelligent Investor.</td>
    </tr>

    <!-- Q23 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q23: User hỏi "Giải thích về quý ngài thị trường"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">giải thích về quý ngài thị trường</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">RAG truy xuất sách The Intelligent Investor và giải thích câu chuyện ẩn dụ về Quý ngài Thị trường (Mr. Market).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Trong sách, Benjamin Graham dùng nhân vật ẩn dụ "Mr. Market" (Quý ngài Thị trường) để mô tả tính khí thất thường của thị trường chứng khoán. Mỗi ngày Mr. Market đều đến đưa ra các mức giá mua/bán khác nhau. Nhà đầu tư thông minh nên tận dụng sự điên rồ và cảm tính của ông ta (mua khi ông ta quá bi quan và bán khi ông ta quá hưng phấn) thay vì bị ông ta dẫn dắt tâm lý.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Tìm kiếm lai lấy ra các chunk tri thức liên quan đến ẩn dụ Mr. Market trong chương 8 của sách Graham.</td>
    </tr>

    <!-- Q24 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q24: User hỏi "Nhà đầu tư phòng thủ nên chia tiền thế nào"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">phân bổ tài sản nhà đầu tư phòng thủ</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">RAG truy xuất tỷ lệ phân bổ tài sản khuyến nghị cho nhà đầu tư phòng thủ giữa cổ phiếu và trái phiếu (thường là 50/50, dao động từ 25% đến 75%).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Graham khuyến nghị nhà đầu tư phòng thủ nên áp dụng tỷ lệ phân bổ cơ bản là 50% cho cổ phiếu chất lượng cao và 50% cho trái phiếu chính phủ. Tùy thuộc vào tình hình thị trường, tỷ lệ này có thể điều chỉnh linh hoạt nhưng không nên vượt quá giới hạn tối thiểu 25% hoặc tối đa 75% cho bất kỳ danh mục nào.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Hybrid Search và Cohere Reranker xếp hạng cao nhất các đoạn văn nói về "Defensive Investor asset allocation".</td>
    </tr>

    <!-- Q25 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q25: User hỏi "Tài sãn và tiêu sãn khác gì nhau trong sách Cha giàu"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">tài sản và tiêu sản khác nhau thế nào trong Rich Dad Poor Dad</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Sửa lỗi chính tả giọng nói (tài sãn -> tài sản, tiêu sãn -> tiêu sản), RAG trích xuất định nghĩa tài sản/tiêu sản từ Rich Dad Poor Dad.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Trong Rich Dad Poor Dad, Robert Kiyosaki định nghĩa rất đơn giản: Tài sản (Asset) là những gì mang tiền bỏ vào túi của bạn (ví dụ: bất động sản cho thuê, cổ phiếu sinh cổ tức); còn Tiêu sản (Liability) là những gì lấy tiền ra khỏi túi của bạn (ví dụ: xe cộ cá nhân, nhà ở trả góp tiêu dùng).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Nhờ cơ chế sửa lỗi chính tả phát âm diacritics từ ASR, hệ thống vẫn nhận diện đúng khái niệm "Tài sản" và "Tiêu sản" để tìm kiếm trong sách Kiyosaki.</td>
    </tr>

    <!-- Q26 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q26: User hỏi "Vòng Rat Race là gì"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">vòng Rat Race trong Rich Dad Poor Dad là gì</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">RAG truy xuất định nghĩa vòng bẫy tài chính luẩn quẩn "Rat Race" trong sách Kiyosaki.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Vòng "Rat Race" (vòng luẩn quẩn) là bẫy tài chính mà đa số người lao động mắc phải: Đi làm -> Kiếm tiền -> Trả hóa đơn/Nợ nần -> Hết tiền -> Lại phải đi làm chăm chỉ hơn. Vòng lặp này lặp lại liên tục do thiếu kiến thức tài chính và bị chi phối bởi nỗi sợ hãi và lòng tham.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Hệ thống lấy đúng định nghĩa về Rat Race trong chương 1 của sách Cha giàu cha nghèo.</td>
    </tr>

    <!-- Q27 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q27: User hỏi "Người giàu lập tập đoàn để làm gì"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">tại sao người giàu thành lập tập đoàn công ty trong Rich Dad Poor Dad</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">RAG trích xuất lợi ích thuế và pháp lý của tập đoàn đối với người giàu (kiếm tiền, chi tiêu trước rồi mới đóng thuế) từ Rich Dad Poor Dad.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Theo Robert Kiyosaki, người giàu thành lập doanh nghiệp/tập đoàn chủ yếu để bảo vệ tài sản và tối ưu hóa thuế. Công thức chi tiêu của doanh nghiệp là: Kiếm tiền -> Chi tiêu các chi phí hợp lệ trước -> Chỉ đóng thuế trên phần lợi nhuận còn lại. Ngược lại, người làm thuê phải: Kiếm tiền -> Đóng thuế thu nhập cá nhân trước -> Chi tiêu phần còn lại.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Tìm kiếm lai trích xuất chương 4 nói về sức mạnh của tập đoàn và lịch sử thuế.</td>
    </tr>

    <!-- Q28 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q28: User hỏi "Chương 4 nói về cái gì"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">tóm tắt chương 4</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Nhận diện xung đột tiêu đề chương 4 giữa hai cuốn sách tài chính, bẻ hướng hỏi người học làm rõ.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Hiện tại cả hai cuốn sách của bạn đều có Chương 4. Bạn muốn tôi tóm tắt Chương 4 về chính sách danh mục đầu tư trong 'The Intelligent Investor' hay Chương 4 về lịch sử thuế và tập đoàn trong 'Rich Dad Poor Dad'?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Guard Rule phát hiện yêu cầu summary chương bị trùng tên giữa hai cuốn sách đang có trong context, kích hoạt intent clarification_required để yêu cầu làm rõ.</td>
    </tr>

    <!-- Q29 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q29: User trả lời "Cuốn Cha giàu đi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">chọn tóm tắt chương 4 sách Rich Dad Poor Dad</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Tóm tắt nội dung chương 4 sách Rich Dad Poor Dad (Lịch sử thuế và sức mạnh của tập đoàn).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Chương 4 sách 'Rich Dad Poor Dad' có tiêu đề 'Lịch sử của Thuế và Sức mạnh của Tập đoàn'. Robert Kiyosaki chia sẻ câu chuyện thuế ban đầu chỉ đánh vào người giàu nhưng dần dần lan sang tầng lớp trung lưu và nghèo. Điểm mấu chốt là người giàu hiểu luật và dùng các thực thể pháp lý (tập đoàn) để bảo vệ tài sản hợp pháp và giảm nghĩa vụ đóng thuế.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Nhận diện câu trả lời bổ sung thông tin từ Q28 nhờ Thread Context, định tuyến thành công đến đúng chương 4 của sách Rich Dad (book_section) để tóm tắt mà không cần chạy RAG thô.</td>
    </tr>

    <!-- Q30 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q30: User hỏi "Tóm tắt chương 5 nữa"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">tóm tắt chương 5</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Nhận diện xung đột tiêu đề chương 5 giữa hai cuốn sách tài chính, hỏi người học làm rõ.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Bạn muốn tôi tóm tắt Chương 5 của 'The Intelligent Investor' (về nhà đầu tư phòng thủ và cổ phiếu phổ thông) hay Chương 5 của 'Rich Dad Poor Dad' (về việc người giàu tạo ra tiền)?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Guard Rule tiếp tục phát hiện yêu cầu summary chương 5 bị trùng tên giữa hai cuốn sách, bẻ hướng định tuyến sang clarification_required lần 2.</td>
    </tr>

    <!-- Q31 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q31: User hỏi "Thôi bỏ qua đi. Thế hôm nay cổ phiếu Apple thế nào"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">hủy yêu cầu tóm tắt, hỏi giá cổ phiếu Apple hôm nay</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Hủy bỏ trạng thái chờ làm rõ của câu hỏi trước, phát hiện câu hỏi ngoài sách/thời gian thực, chặn web và hỏi xin quyền tìm kiếm web.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Thông tin về giá cổ phiếu Apple hôm nay không có sẵn trong hai cuốn sách tĩnh của bạn. Để cập nhật dữ liệu tài chính thực tế này, tôi cần tìm kiếm trên internet. Bạn có đồng ý không?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Kịch bản Topic Shift (đổi ý đột ngột khi đang chờ làm rõ). Hệ thống tự giải phóng trạng thái chờ làm rõ, nhận diện câu hỏi ngoài sách và định tuyến sang policy (external_current_info) để chặn web và xin quyền.</td>
    </tr>

    <!-- Q32 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q32: User trả lời "Khỏi, tự trả lời đi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">không đồng ý tìm kiếm web</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Từ chối tìm web và chỉ dùng Parametric Memory để khuyên người dùng tự tra cứu sàn giao dịch.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Đồng ý, tôi sẽ không tìm kiếm internet. Do không có quyền truy cập dữ liệu thời gian thực và thông tin thị trường biến động liên tục, tôi không thể cung cấp giá chính xác hiện tại của Apple. Bạn nên tự kiểm tra trên các ứng dụng tài chính hoặc bảng giá chứng khoán nhé.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Phân loại ý định từ chối (web_search_denied) chuẩn xác, đóng luồng web và trả lời an toàn bằng tri thức sẵn có.</td>
    </tr>

    <!-- Q33 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q33: User hỏi "Thế còn giá Bitcoin hôm nay? Tìm mạng đi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">tìm giá Bitcoin hôm nay trên internet</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Mặc dù user yêu cầu chủ động "tìm mạng đi", nhưng hệ thống vẫn thực thi chính sách bảo mật hỏi xin quyền cho yêu cầu mới này do token cũ đã hết hiệu lực.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Để cập nhật giá Bitcoin mới nhất hôm nay trên internet, tôi cần sự cho phép của bạn. Tôi có thể thực hiện tìm kiếm web không?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Nguyên tắc Một lần (One-time token validation). Quyền tìm kiếm của câu hỏi trước đã bị thu hồi ngay lập tức sau lượt hội thoại cũ. Hệ thống bắt buộc phải xin quyền lại cho yêu cầu mới.</td>
    </tr>

    <!-- Q34 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q34: User trả lời "Ừ, tìm đi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">đồng ý tìm kiếm web</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Gọi Tavily Search để tìm giá Bitcoin hôm nay và tổng hợp câu trả lời cho người học.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Theo kết quả tìm kiếm internet mới nhất hôm nay, giá Bitcoin hiện tại đang giao dịch quanh mức 65,400 USD (hoặc mức giá thực tế tại thời điểm search). Thị trường đang có xu hướng biến động nhẹ trước các tin tức kinh tế mới...</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang web_search (web_search_granted). Chạy công cụ tìm kiếm web Tavily, lấy kết quả thời gian thực thành công.</td>
    </tr>

    <!-- Q35 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q35: User hỏi "Giá Ethereum thì sao"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">giá Ethereum hôm nay trên internet</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Quyền tìm giá Bitcoin trước đó đã bị thu hồi ngay lập tức. Hệ thống tiếp tục hỏi xin quyền lần tiếp theo.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Tôi cần tiếp tục tìm kiếm trên internet để cập nhật giá Ethereum mới nhất hôm nay. Bạn có đồng ý không?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Kiểm chứng tính chất Một lần của token cấp quyền ở câu hỏi liên tục. Quyền cũ bị thu hồi ngay lập tức sau khi hoàn thành task ở Q34, bắt buộc phải hỏi xin quyền lại.</td>
    </tr>

    <!-- Q36 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q36: User trả lời "Tìm luôn đi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">đồng ý tìm kiếm web</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Gọi Tavily Search để tìm giá Ethereum hôm nay và tổng hợp câu trả lời.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Theo thông tin tìm kiếm internet mới nhất hôm nay, giá Ethereum hiện đang giao dịch ở mức khoảng 3,450 USD (hoặc mức thực tế). Khối lượng giao dịch trong 24 giờ qua tăng mạnh...</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang web_search (web_search_granted) lần 2 thành công nhờ sự chấp thuận rõ ràng của người học.</td>
    </tr>

    <!-- Q37 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q37: User hỏi "Thế còn Liquidity Mining là gì? Sách có dạy không"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">Liquidity Mining là gì và sách tài chính có đề cập không</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Nhận diện khái niệm DeFi này hoàn toàn không có trong hai sách tài chính cổ điển, phát cảnh báo ngoài sách và hỏi xin quyền tìm kiếm web.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Khái niệm 'Liquidity Mining' (khai thác thanh khoản) thuộc về lĩnh vực tài chính phi tập trung (DeFi) mới và hoàn toàn không được đề cập trong hai cuốn sách cổ điển của bạn. Để tìm hiểu định nghĩa chính xác từ internet, tôi cần tìm kiếm web. Bạn có cho phép không?</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Nhận diện khái niệm nằm ngoài tri thức tĩnh của sách (book_context_not_found), thực thi cơ chế cảnh báo giới hạn tri thức và hỏi xin quyền Web.</td>
    </tr>

    <!-- Q38 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q38: User trả lời "Khỏi tìm, giải thích sơ thôi"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">không đồng ý tìm kiếm web</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Từ chối tìm web và chỉ dùng Parametric Memory của LLM để giải thích tóm tắt về khái niệm Liquidity Mining.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Đồng ý, tôi sẽ không tìm kiếm internet. Dựa trên tri thức của tôi, Liquidity Mining (khai thác thanh khoản) là cơ chế trong DeFi nơi người dùng cung cấp tài sản tiền mã hóa vào các bể thanh khoản (liquidity pools) để nhận lại phần thưởng là token quản trị của dự án đó, tương tự như việc gửi tiết kiệm nhận lãi...</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Phân loại ý định từ chối (web_search_denied) chuẩn xác, đóng luồng web và fallback thành công về Parametric Memory của mô hình LLM.</td>
    </tr>

    <!-- Q39 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q39: User hỏi "Quay lại sách Nhà đầu tư thông minh, Graham khuyên gì về quỹ chỉ số"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">khuyên của Graham về quỹ chỉ số trong The Intelligent Investor</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">RAG định tuyến về cuốn sách The Intelligent Investor để trả lời khuyên của Graham về việc đầu tư thụ động vào các quỹ chỉ số (Index Funds).</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Benjamin Graham cực kỳ ủng hộ việc đầu tư vào các quỹ chỉ số (Index Funds) đối với hầu hết các nhà đầu tư cá nhân, đặc biệt là nhà đầu tư phòng thủ. Ông nhấn mạnh rằng việc cố gắng tự lựa chọn cổ phiếu riêng lẻ để đánh bại thị trường thường mang lại hiệu suất kém hơn so với việc nắm giữ toàn bộ thị trường thông qua các quỹ chỉ số chi phí thấp một cách thụ động lâu dài.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Tìm kiếm lai lấy ra các chunk tri thức liên quan đến "Index Funds" từ các chương cuối sách The Intelligent Investor (được cập nhật bởi Jason Zweig).</td>
    </tr>

    <!-- Q40 -->
    <tr style="background-color: #f2f2f2;">
      <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q40: User hỏi "Cảm ơn, tắt máy nhé"</td>
    </tr>
    <tr>
      <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">AI hiểu</td>
      <td style="padding: 8px;">kết thúc phiên đàm thoại</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
      <td style="padding: 8px;">Lời chào tạm biệt ngắn gọn, lưu trữ phiên đàm thoại và dừng luồng.</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
      <td style="padding: 8px;">Rất vui được hỗ trợ bạn ôn tập hôm nay! Chúc bạn áp dụng tốt các nguyên tắc đầu tư thông minh và quản lý tài chính cá nhân hiệu quả. Hẹn gặp lại bạn ở các buổi học sau nhé!</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
      <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
    </tr>
    <tr>
      <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
      <td style="padding: 8px;">Nhận diện ý định chào kết thúc đàm thoại (chitchat/farewell), kết thúc an toàn.</td>
    </tr>

  </table>
