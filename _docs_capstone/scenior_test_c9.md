# Kịch Bản Đánh Giá Thực Nghiệm Đa Lượt Giọng Nói (Multi-Turn Voice Session)

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
      <b>(Ví dụ về việc mô tả ngữ cảnh)</b><br>
      - 1 context gồm 2 tài liệu: <i>Of Mice and Men</i> và <i>Chương 4 hướng dẫn dùng RAG</i><br>
      - <i>Of Mice and Men</i>: nói về cuộc đời của các nhân vật và các tình tiết vui buồn lẫn lộn trong thời kì khó khăn của tầng lớp lao động thời kỳ Đại suy thoái.<br>
      - <i>Chương 4 hướng dẫn dùng RAG</i>: nói về cách thức cấu hình và sử dụng công nghệ tìm kiếm tri thức bám nguồn RAG.
    </td>
  </tr>

  <!-- Q1 -->
  <tr style="background-color: #f2f2f2;">
    <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q1: User hỏi "Sách có mấy chương"</td>
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
      - <b>Mục tiêu</b>: Đánh giá khả năng phân tách tri thức, chống nhiễu chéo RAG khi hai tài liệu có các từ khóa và khái niệm kỹ thuật trùng lặp cao (arrays, functions, trees).
    </td>
  </tr>

  <!-- Q11 -->
  <tr style="background-color: #f2f2f2;">
    <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q11: User hỏi "Tôi muốn tìm hiểu về C# và thuật toán"</td>
  </tr>
  <tr>
    <td style="width: 15%; padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
    <td style="padding: 8px;">Chào đón người dùng và liệt kê chính xác 2 tài liệu IT đang có trong Study Context.</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
    <td style="padding: 8px;">Chào bạn! Tôi rất sẵn lòng hỗ trợ. Hiện tại Study Context của bạn đang liên kết với hai tài liệu: 'Algorithms Notes for Professionals' (257 trang) và 'C# programming example and solutions' (68 trang). Bạn muốn bắt đầu ôn tập phần nào?</td>
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
    <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q12: User hỏi "Có những thuật toán nào dành cho người mới"</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
    <td style="padding: 8px;">Liệt kê các thuật toán cơ bản dành cho người mới từ cuốn 'Algorithms Notes for Professionals' (Bubble Sort, Binary Search, Big-O...).</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
    <td style="padding: 8px;">Dựa trên tài liệu Algorithms Notes for Professionals, đối với người mới bắt đầu, bạn nên làm quen với các khái niệm ở Chapter 1 (Khởi đầu với thuật toán), Chapter 2 (Độ phức tạp thuật toán) và Chapter 3 (Ký hiệu Big-O). Các thuật toán sắp xếp cơ bản như Bubble Sort, Selection Sort hoặc tìm kiếm nhị phân (Binary Search) là điểm khởi đầu tốt...</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
    <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
    <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Hệ thống thực hiện Hybrid Search lấy ra các chunk tri thức giới thiệu thuật toán cho người mới từ tài liệu Algorithms và Cohere Reranker xếp hạng cao nhất.</td>
  </tr>

  <!-- Q13 -->
  <tr style="background-color: #f2f2f2;">
    <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q13: User trả lời "Linh qui trong C# là gì"</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
    <td style="padding: 8px;">Định nghĩa và giải thích tính năng LINQ (Language Integrated Query) trong C# (Topic 7 của sách C#).</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
    <td style="padding: 8px;">Trong C#, LINQ (viết tắt của Language Integrated Query - truy vấn tích hợp ngôn ngữ) là một tính năng mạnh mẽ được giới thiệu từ .NET 3.5. Nó cho phép bạn viết các câu lệnh truy vấn dữ liệu trực tiếp trong mã nguồn C# để lọc, tìm kiếm và thao tác trên nhiều nguồn dữ liệu khác nhau (như Collections, XML, hay Database) tương tự như SQL...</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
    <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
    <td style="padding: 8px;">Định tuyến sang RAG (book_rag). Dù người dùng gõ sai chính tả ("Linh qui" thay vì "LINQ"), hệ thống nhờ cơ chế chuẩn hóa từ khóa và tìm kiếm lai vẫn nhận diện chính xác tri thức cần tìm là LINQ trong tài liệu C# programming example and solutions (Topic 7).</td>
  </tr>

  <!-- Q14 -->
  <tr style="background-color: #f2f2f2;">
    <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q14: User hỏi "Các thuật toán nào làm nền tảng cho AI vậy. Tôi muốn theo AI thì học như nào. Hiện tại tôi chỉ tìm được các tài liệu như trên"</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
    <td style="padding: 8px;">Giải thích các thuật toán AI nền tảng (như Gradient Descent, Backpropagation) không có sẵn trong 2 tài liệu hiện tại, tư vấn lộ trình học AI sử dụng kiến thức nền toán học và lập trình.</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
    <td style="padding: 8px;">Các thuật toán nền tảng cho AI như Gradient Descent, Backpropagation, hay các mạng Neural Network hiện tại không nằm trong hai cuốn sách trong Study Context của bạn (vốn chỉ nói về thuật toán cấu trúc dữ liệu cơ bản và lập trình C#). Để theo học AI, bạn nên nắm vững Toán (Đại số tuyến tính, Xác suất thống kê), sau đó học các thuật toán Học máy. Bạn có muốn tôi tìm kiếm lộ trình chi tiết hơn từ internet không?</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
    <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
    <td style="padding: 8px;">Định tuyến sang policy (external_current_info) kết hợp parametric memory. Hệ thống nhận diện câu hỏi nằm ngoài phạm vi tri thức sách hiện tại, đưa ra cảnh báo giới hạn tri thức và hỏi xin quyền tìm kiếm web.</td>
  </tr>

  <!-- Q15 -->
  <tr style="background-color: #f2f2f2;">
    <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q15: User hỏi "Hiện nay 2026 Microsoft đã phát hành phiên bản .NET và C# mới nhất là bản mấy và có tính năng gì nổi bật?"</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
    <td style="padding: 8px;">Nhận diện câu hỏi thông tin thời gian thực năm 2026 ngoài sách, yêu cầu tra cứu internet và hỏi xin quyền tìm kiếm web.</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
    <td style="padding: 8px;">Để cập nhật thông tin về phiên bản .NET và C# mới nhất của Microsoft tính đến năm 2026, tôi cần tìm kiếm trên internet. Bạn có cho phép tôi tra cứu web không?</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
    <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
    <td style="padding: 8px;">Định tuyến sang policy (external_current_info). Hệ thống phát hiện thông tin thời gian thực ngoài sách, thực thi chính sách chặn Web và hỏi xin ý kiến người dùng.</td>
  </tr>

  <!-- Q16 -->
  <tr style="background-color: #f2f2f2;">
    <td colspan="2" style="padding: 8px; font-weight: bold; text-align: left;">Q16: User trả lời "Được, hãy tra cứu giúp tôi"</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Đáp Án</td>
    <td style="padding: 8px;">Gọi Tavily Search để tìm kiếm thông tin .NET và C# mới nhất (đến năm 2026, ví dụ .NET 10 / C# 14) và tổng hợp câu trả lời.</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">AI trả lời</td>
    <td style="padding: 8px;">Theo kết quả tìm kiếm internet cập nhật đến năm 2026, Microsoft đã phát hành phiên bản .NET 10 (hoặc .NET 9 mới nhất). Các tính năng nổi bật của C# 14 / C# 13 bao gồm tối ưu hóa hiệu năng AoT, cải tiến collection expressions và primary constructors...</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Kết quả</td>
    <td style="padding: 8px; color: green; font-weight: bold;">Đạt</td>
  </tr>
  <tr>
    <td style="padding: 8px; font-weight: bold; background-color: #fafafa;">Lý do</td>
    <td style="padding: 8px;">Định tuyến sang web_search (web_search_granted). Chạy công cụ tìm kiếm web Tavily, lấy kết quả thời gian thực và tổng hợp câu trả lời thành công.</td>
  </tr>
</table>
