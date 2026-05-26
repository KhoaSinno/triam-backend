## Page 1

Chương 3.
PHÂN TÍCH THIẾT KẾ HỆ THỐNG

1. Sơ đồ
   1.1. Sơ đồ tổng quan
   Một khung thức được nhóm nghiên cứu đề xuất để thể hiện rõ ràng các thành phần trong hệ thống như Hình 3.1. Đây là cơ sở để hiện thực hóa các mục tiêu của nhóm. Khung thức gồm các thành phần sau: Mô-đun quản lý file PDF, Phân quyền. Hệ thống sẽ được sử dụng với ba vai trò người dùng là Cán bộ, Giảng viên và Sinh viên.

&lt;img&gt;
A flowchart diagram illustrating a system architecture for a document management and AI-based information retrieval system.
The diagram shows the following components and their interactions:

- **Users:** Cán bộ (Staff), Giảng viên (Lecturer), Sinh viên (Student).
- **System Modules:**
  - Modun quản lý file pdf (PDF file management module)
  - Phân quyền (Authorization)
  - Machine Learning Studio Workspaces
  - CSDL JSON hỏi trả lời (JSON database for questions and answers)
  - Chat với AI (Chat with AI)
- **External Systems/Technologies:**
  - php, JS, LangChain (indicated as technologies used in the system)
  - Máy chủ lưu trữ file (File storage server)
  - LLM Chain (Large Language Model Chain)
- **Data Flow:**
  _ Users send PDFs via HTTP to the PDF file management module.
  _ The system uses API học từ pdf (API learning from PDF) and API học từ json (API learning from JSON) to process data.
  _ The system can send and receive JSON data.
  _ The Chat with AI component interacts with the LLM Chain.
  _ The LLM Chain can be queried with questions like "HTTT là gì?" (What is HTTT?) and receives answers.
  _ The system can send and receive questions and answers.
  &lt;/img&gt;
  | Thành phần (Component) | Chức năng / Kết nối (Function / Connection) |
  | :--- | :--- |
  | Cán bộ | Gửi file PDF qua HTTP đến Mô-đun quản lý file PDF |
  | Giảng viên | Gửi câu hỏi và nhận trả lời từ Chat với AI |
  | Sinh viên | Gửi câu hỏi và nhận trả lời từ Chat với AI |
  | Mô-đun quản lý file PDF | Lưu trữ bản sao PDF lên Máy chủ lưu trữ file; Kết nối với Phân quyền; API học từ PDF |
  | Phân quyền | Quản lý quyền truy cập trong hệ thống |
  | Máy chủ lưu trữ file | Lưu trữ các tệp PDF |
  | Machine Learning Studio Workspaces | Cung cấp môi trường làm việc cho học máy; Kết nối với CSDL JSON |
  | CSDL JSON hỏi trả lời | Lưu trữ dữ liệu câu hỏi và trả lời; API học từ JSON |
  | Chat với AI | Giao diện tương tác người dùng; Kết nối với LLM Chain |
  | LLM Chain | Xử lý ngôn ngữ tự nhiên; Gửi câu hỏi/nhận trả lời qua API của LLM Chain |
  | Công nghệ sử dụng | php, JS, LangChain |

Hình 3.1: Sơ đồ tổng quan hỗ trợ sinh viên tra cứu thông tin dựa trên AI

Từ Hình 3.1 các thành phần được diễn giải như sau:

&lt;page_number&gt;21&lt;/page_number&gt;

---

## Page 2

Xây dựng ứng dụng học máy hỗ trợ thủ tục hành chính cho sinh viên

- **Mô-đun quản lý file PDF:** Mô-đun này thực hiện chức năng Quản lý các file PDF nhận được từ cán bộ và xử lý. Sau khi nhận được các file từ cán bộ, Mô-đun này sẽ gửi yêu cầu đến phân quyền để xác nhận rằng cán bộ này có quyền tải PDF lên hay không. Sau đó Mô-đun quản lý file PDF sẽ gửi file đến máy chủ lưu trữ file PDF.
- **Cán bộ:** Vai trò cán bộ sẽ có thể upload những tài liệu PDF lên hệ thống và từ đó hệ thống sẽ sao chép một bản sao để lưu lại và thư mục riêng và file chính sẽ được xử lý thông qua các Framework và mô hình ngôn ngữ để đọc hiểu và lưu lại dưới dạng file json.
- **Sinh Viên:** Với người dùng là Sinh viên có thể hỏi đáp các thắc mắc thông qua Chatbot để có thể nhận được thông tin cần thiết mà không cần phải tìm kiếm các file PDF của trường.
- **Giảng viên:** Tương tự với Sinh viên, Giảng viên cũng có thể hỏi đáp các thắc mắc cũng như các quy định về hành chính của trường thông qua Chatbot để có thể nhận được thông tin cần thiết mà không cần phải tự tìm các file PDF của trường
- **Phân quyền:** Quản lý quyền truy cập và xử lý các yêu cầu từ các thành phần khác trong hệ thống, chức năng có thể chỉnh sửa và điều hành bởi cán bộ.
- **Hỏi đáp với AI:** Hệ thống chatbot AI, nhận câu hỏi từ giảng viên và sinh viên sau đó sẽ gửi API đến LLMs chain để trích xuất dữ liệu phù hợp và gửi về câu trả lời cho hệ thống chatbot AI và hệ thống sẽ hiển thị dữ liệu đó cho người dùng.
- **Không gian làm việc của máy học:** Sau khi trả lời người dùng và được đánh giá các câu trả lời, Mô-đun này tương tác với cơ sở dữ liệu JSON hỏi trả lời để cung cấp kết quả đánh giá cho cơ sở dữ liệu JSON và sắp xếp mức độ hữu ích của câu trả lời.
- **Cơ sở dữ liệu JSON:** Lưu trữ và quản lý các câu hỏi và câu trả lời được đánh giá dưới dạng JSON. Cung cấp API học từ JSON cho hệ thống và ưu tiên các câu trả lời đã được đánh giá cao trước đó để trả lời.
- **JSON:** Định dạng lưu trữ cơ sở dữ liệu hỏi đáp trong hệ thống, của người dùng theo thời gian và ngày trò chuyện
- **LLM Chain:** Chuỗi mô hình ngôn ngữ lớn, xử lý các tài liệu PDF được lưu trữ trên máy chủ và xử lý các yêu cầu học hỏi và trả lời câu hỏi từ hệ thống
- **LangChain, Python, PHP, JS, MySQL:** Các ngôn ngữ lập trình và Framework được sử dụng để phát triển và quản lý hệ thống.

&lt;page_number&gt;22&lt;/page_number&gt;

---

## Page 3

Xây dựng ứng dụng học máy hỗ trợ thủ tục hành chính cho sinh viên

2. Đặc tả hệ thống

Chức năng hệ thống:

- **Kiến trúc tổng thể:** Ứng dụng học máy hỗ trợ thủ tục hành chính là một trang web ứng dụng nhiều công nghệ và ngôn ngữ lập trình khác nhau như Python, PHP, JavaScript đặc biệt là LangChain để kết nối hợp lại và xây dựng nên một ứng dụng học máy này một trang web hỗ trợ hành chính để giải đáp các thắc mắc về vấn đề liên quan về mặt hành chính như: Học phí, quá trình nhập học, các ngành mà trường nhận đào tạo cho tân sinh viên và cũng như những thông báo, quy định, nghị định cho giảng viên mới vào trường.

- **Backend:** Sử dụng PHP và Python làm ngôn ngữ lập trình chính cho Backend và Flask để xây dựng nên chatbot. Bắt đầu từ việc sử dụng Python để gọi API từ OpenAI để chạy chức năng cho chatbot cụ thể hơn là xử lý dữ liệu hoặc thực hiện các tác vụ máy học, gửi và truy xuất dữ liệu sau đó các dữ liệu được truy xuất sẽ hiển thị lên giao diện của cán bộ, sinh viên, giảng viên.

  Ở giao diện của cán bộ sẽ có thêm Mô-đun quản lý file PDF, Mô-đun này có thể lưu trữ các tài liệu được cán bộ tải lên và được sử dụng làm kho dữ liệu dành cho chatbot học hỏi để phục vụ cho ứng dụng hỗ trợ thủ tục hành chính.

  Một khi cán bộ, sinh viên, giảng viên đã sử dụng ứng dụng để hỏi đáp xoay quanh vấn đề hành chính thì dữ liệu của đoạn hội thoại sẽ được lưu lại dưới định dạng dữ liệu JSON.

- **Frontend:** Để trình bày một giao diện thân thiện mang lại cho người dùng cảm nhận được sự gần gũi khi tương tác với ứng dụng thì nhóm đã sử dụng kết hợp giữa HTML, CSS và PHP để xây dựng một giao diện cụ thể và có giao diện cho cả cán bộ, giảng viên và sinh viên. Sử dụng HTML, CSS, PHP cho tương tác phía người dùng. Có giao diện cho cả giảng viên và sinh viên.

- **Xử lý ngôn ngữ tự nhiên:** Bằng việc sử dụng Framework LangChain và các thư viện từ LangChain, để xử lý, đọc và phân tích văn bản từ file nên khi ứng dụng được đưa vào thực tế thì chatbot đã cho được tỉ lệ trả lời đúng đạt trên 94%. Đối với ứng dụng này thì vai trò của cán bộ sẽ rất quan trọng vì cán bộ sẽ là người kiểm tra các file văn bản phải được đưa vào xử lý và biến thành cơ sở dữ liệu dành cho chatbot để trả lời.

&lt;page_number&gt;23&lt;/page_number&gt;

---

## Page 4

Xây dựng ứng dụng học máy hỗ trợ thủ tục hành chính cho sinh viên

Sử dụng LangChain, để có thể xử lý và phân tích văn bản. Có "Máy chủ kéo file" có thể liên quan đến việc xử lý và trích xuất thông tin từ file PDF.

- **Luồng dữ liệu:** Về luồng dữ liệu và kho dữ liệu, cán bộ sẽ là người chịu trách nhiệm tải lên các file PDF và duyệt các file nào có thể được tải lên, giữ lại hoặc xóa khi đi có file khác cùng nội nhưng là thông báo mới hơn. Sau khi cán bộ đã quyết định được nên tải file dữ liệu lên thì hệ thống kết hợp xử lý ngôn ngữ tự nhiên và trích xuất những thông tin có được từ file dữ liệu và lưu vào Cơ sở dữ liệu.

Sau khi cán bộ tải lên những dữ liệu mới nhất thì sinh viên và giảng viên có thể truy vấn thông tin thông qua hỏi đáp với chatbot để biết được thông tin cần thiết. Việc có thể xử lý, trao đổi giữa Frontend và Backend khi ứng dụng đang thực hiện thì hệ thống đã sử dụng API để giúp việc trao đổi, lưu thông ổn định hơn trong quá trình sử dụng.

- **Tính năng bảo mật:** Trong quá trình thực hiện thì nhóm xác định được rằng, chỉ có cán bộ mới được quyền xử lý và tải các dữ liệu lên nên thực hiện thêm Mô-đun phân quyền để tăng tính bảo mật, tránh các việc, hành vi vô tình đến từ sinh viên và giảng viên.

- **Tích hợp API:** Việc tích hợp API từ các nguồn vào Python để sử dụng và xây dựng được hệ thống thì nhóm không chỉ sử dụng API từ OpenAI, thêm vào đó là API từ LLMChain để có thể tích hợp mô hình ngôn ngữ lớn, và API riêng cho việc xử lý các file PDF và JSON.

- **Xử lý đa ngôn ngữ:** Việc xử lý đa ngôn ngữ của trí tuệ nhân tạo được thực hiện bằng cách, khi người dùng nhập một thông tin vào bằng một ngôn ngữ bất kỳ với công nghệ học máy sẽ tự động hiểu và luôn xuất ra kết quả bạn cần bằng tiếng Việt.

- **Giao diện người dùng:** Hiện tại trong hệ thống ứng dụng được chia ra giao diện khác nhau, một giao diện là dành riêng cho cán bộ với các chức năng có thể thao tác lên các file tài liệu và một giao diện là dành riêng cho giảng viên và sinh viên để tương tác với hệ thống.

- **Lưu trữ và quản lý file:** Để hệ thống ứng dụng có thể hoạt động trơn tru thì hệ thống lưu trữ và quản lý file cũng là một phần quan trọng trong hệ thống vì đây là nơi để truyền dữ liệu và học hỏi của chatbot.

Sử dụng CSDL JSON để lưu trữ dữ liệu có cấu trúc.

&lt;page_number&gt;24&lt;/page_number&gt;

---

## Page 5

Xây dựng ứng dụng học máy hỗ trợ thủ tục hành chính cho sinh viên

**Chức năng phi hệ thống:**

- Để cải thiện thiết kế này, có thể cân nhắc: Sau khi nhóm đã bắt đầu thực hiện đề tài "Xây dựng ứng dụng học máy hỗ trợ thủ tục hành chính cho sinh viên" và đưa đề tài vào thực tế để kiểm tra và hoạt động thì sau đây là những gì mà nhóm nghĩ rằng Hệ thống ứng dụng này có thể cải thiện để có thể trở thành một sản phẩm hoàn thiện hơn.
- Thêm lớp bảo mật cho API và xác thực người dùng.
- Tối ưu hóa hiệu suất xử lý file PDF lớn.
- Thiết kế hệ thống có khả năng mở rộng để xử lý lượng truy cập lớn.
- Triển khai hệ thống dự phòng và khôi phục dữ liệu.
- Chỉnh sửa giao diện có thể chuyển đổi tiếng Anh và tiếng Việt.

**3. Sơ đồ Usecase**

&lt;img&gt;
A UML Use Case Diagram showing two actors: Admin (purple), Teacher (red), and Student (blue). The Admin interacts with the FileManage use case. FileManage includes UploadFile, DeleteFile, Login, and Permission. The AI use case includes PDFs, Embeddings, LLM, and ExportJson. ChatwithAI includes Login and ExportJson. The Teacher and Student actors interact with the ChatwithAI use case.
&lt;/img&gt;
| Actor | Use Case | Relationship | Target Use Case |
| :--- | :--- | :--- | :--- |
| Admin | FileManage | — | — |
| Teacher | ChatwithAI | — | — |
| Student | ChatwithAI | — | — |
| — | FileManage | Include | UploadFile |
| — | FileManage | Include | DeleteFile |
| — | FileManage | Include | Permission |
| — | FileManage | Include | Login |
| — | AI | Include | PDFs |
| — | AI | Include | Embeddings |
| — | AI | Include | LLM |
| — | ChatwithAI | Include | Login |
| — | ChatwithAI | Include | ExportJson |

Hình 3.2: Sơ đồ Usecase

**3.1. Đặc tả Usecase**

**Cán bộ:** Là chức vụ cao nhất trong hệ thống và có chức năng như sau:

&lt;page_number&gt;25&lt;/page_number&gt;

---

## Page 6

Xây dựng ứng dụng học máy hỗ trợ thủ tục hành chính cho sinh viên

- **Quản lý file:** Cán bộ có thể toàn quyền thêm và xóa file PDF trong hệ thống.
- **Phân quyền:** Chức năng có thể cho phép cán bộ phân chia chức vụ của các người dùng tham gia hệ thống.

**Sinh viên:** Người dùng được để tâm nhất trong hệ thống, là người dùng tham gia hệ thống đông đảo và thường xuyên.

- **Trò chuyện với AI:** Sinh viên được cung cấp một tài khoản từ phía nhà trường để có thể dễ dàng tham gia vào hệ thống và sử dụng tính năng chat.

**Giảng viên:** Tương tự như Sinh Viên, Giảng viên cũng được cung cấp một tài khoản có thể tham gia vào hệ thống và tương tác với hệ thống.

- **Trò chuyện với AI:** Giảng viên có thể sử dụng chức năng chat với AI bằng tài khoản được cung cấp bởi trường đại học.

**AI:** Đóng vai trò cốt lõi trong hệ thống, được xây dựng với tiêu chí hỗ trợ không ngừng nghỉ cho người dùng các thành phần mà AI xử lý sau khi nhận được văn bản từ người dùng như sau:

- **LLM:** Là ngôn ngữ lớn để hiểu được ngữ cảnh của mạch chuyện câu hỏi người dùng là việc không thể thiếu.
- **Embeddings:** Mỗi văn bản sẽ được số hóa có thể lên đến hàng nghìn hàng triệu mã số, vì vậy với quá trình này sẽ giúp máy học có thể tìm kiếm văn bản nhanh hơn.
- **PDFs:** Là một bộ tư liệu về hành chính được đóng gói trong một thư mục, AI sẽ lấy tài liệu được cung cấp trong đây để trả lời chính xác cho người dùng.

&lt;page_number&gt;26&lt;/page_number&gt;

---

## Page 7

Xây dựng ứng dụng học máy hỗ trợ thủ tục hành chính cho sinh viên

4. Sơ đồ Lớp

&lt;img&gt;
A UML class diagram showing the relationships between classes. At the top, there is a class named "Tài Khoản" with attributes "Tentaikhoan: String" and "Matkhau: String". Below it, three classes inherit from "Tài Khoản": "Sinh viên", "Cán bộ", and "Giáo viên". Each of these classes has attributes "userID: String", "HovaTen String", "NgaySinh: Date", "Email: String", and "Chucvu: String". The "Cán bộ" class also has methods "PhanQuyen()", "ThemFile()", and "XoaFile()". To the right of "Tài Khoản", there is a class "Chatbot" with attributes "Cauhoi: String" and "Cautraloi: String", and a method "Taodoanchat()". An arrow from "Tài Khoản" to "Chatbot" is labeled "0..1" and "1". Above "Chatbot", there is a class "Pdf" with an arrow labeled "n" pointing to "Chatbot".
&lt;/img&gt;
| Class Name | Attributes | Methods | Relationships |
| :--- | :--- | :--- | :--- |
| Tài Khoản | Tentaikhoan: String, Matkhau: String | — | Parent of Sinh viên, Cán bộ, Giáo viên; 0..1 to 1 Chatbot |
| Sinh viên | userID: String, HovaTen: String, NgaySinh: Date, Email: String, Chucvu: String | — | Inherits from Tài Khoản |
| Cán bộ | userID: String, HovaTen: String, NgaySinh: Date, Email: String, Chucvu: String | PhanQuyen(), ThemFile(), XoaFile() | Inherits from Tài Khoản |
| Giáo viên | userID: String, HovaTen: String, NgaySinh: Date, Email: String, Chucvu: String | — | Inherits from Tài Khoản |
| Chatbot | Cauhoi: String, Cautraloi: String | Taodoanchat() | 1 to 0..1 Tài Khoản; n from Pdf |
| Pdf | — | — | n to Chatbot |

Hình 3.3: Sơ đồ Lớp

Hình 3.3 mô tả một sơ đồ UML (Unified Modeling Language) thể hiện mối quan hệ giữa các đối tượng trong một hệ thống quản lý tài khoản người dùng.

Cụ thể, sơ đồ bao gồm các thành phần sau:

- Tài khoản: Đây là lớp cha (superclass) chứa các thuộc tính chung cho mọi loại tài khoản, bao gồm TenTaiKhoan (tên tài khoản) và MatKhau (mật khẩu).
- Sinh viên, Cán bộ, Giáo viên: Đây là các lớp con (subclass) kế thừa từ lớp Tài khoản, đại diện cho các loại người dùng khác nhau trong hệ thống. Mỗi lớp con có thêm các thuộc tính riêng như HovaTen (họ và tên), NgaySinh (ngày sinh), Email (địa chỉ email) và Chucvu (chức vụ).

&lt;page_number&gt;27&lt;/page_number&gt;

---

## Page 8

Xây dựng ứng dụng học máy hỗ trợ thủ tục hành chính cho sinh viên

- Cán bộ: Lớp này có thêm các phương thức (method) PhanQuyen() (phân quyền), ThemFile() (thêm tệp) và XoaFile() (xóa tệp), cho thấy cán bộ có quyền quản lý tài khoản và tệp tin trong hệ thống.
- Chatbot: Đây là một lớp độc lập, có chức năng TaoDoanChat() (tạo đoạn chat), có thể được sử dụng để hỗ trợ người dùng tương tác với hệ thống.
- Pdf: Đây là một lớp độc lập, đại diện cho các tệp tin PDF trong hệ thống.

Các mối quan hệ giữa các lớp được biểu diễn bằng các đường nối và các ký hiệu:

- Mũi tên kế thừa: Biểu thị mối quan hệ kế thừa (inheritance), ví dụ, lớp Sinh viên kế thừa từ lớp Tài khoản.
- Mũi tên liên kết: Biểu thị mối quan hệ liên kết (association), ví dụ, Tài khoản liên kết với Chatbot.
- Số “1” và “n”: Biểu thị số lượng đối tượng tham gia vào mối quan hệ, ví dụ, 1 Tài khoản có thể liên kết với nhiều (n) Chatbot.

Chi tiết các thuộc tính trong mỗi lớp sẽ được thể hiện trong bảng sau:

&lt;page_number&gt;28&lt;/page_number&gt;

---

## Page 9

Xây dựng ứng dụng học máy hỗ trợ thủ tục hành chính cho sinh viên

<table>
  <thead>
    <tr>
      <th>Lớp</th>
      <th>Thuộc tính</th>
      <th>Kiểu dữ liệu</th>
      <th>Mô tả</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="4">Sinh Viên</td>
      <td>userID</td>
      <td>String</td>
      <td>Mã định danh người dùng</td>
    </tr>
    <tr>
      <td>HovaTen</td>
      <td>String</td>
      <td>Họ tên người tham gia hệ thống</td>
    </tr>
    <tr>
      <td>NgaySinh</td>
      <td>Date</td>
      <td>Ngày sinh của người tham gia hệ thống</td>
    </tr>
    <tr>
      <td>Email</td>
      <td>String</td>
      <td>Email của người tham gia hệ thống</td>
    </tr>
    <tr>
      <td rowspan="4">Cán bộ</td>
      <td>Chucvu</td>
      <td>String</td>
      <td>Chức vụ người tham gia hệ thống</td>
    </tr>
    <tr>
      <td>userID</td>
      <td>String</td>
      <td>Mã định danh người dùng</td>
    </tr>
    <tr>
      <td>HovaTen</td>
      <td>String</td>
      <td>Họ tên người tham gia hệ thống</td>
    </tr>
    <tr>
      <td>NgaySinh</td>
      <td>Date</td>
      <td>Ngày sinh của người tham gia hệ thống</td>
    </tr>
    <tr>
      <td rowspan="4">Giảng viên</td>
      <td>Email</td>
      <td>String</td>
      <td>Email của người tham gia hệ thống</td>
    </tr>
    <tr>
      <td>Chucvu</td>
      <td>String</td>
      <td>Chức vụ người tham gia hệ thống</td>
    </tr>
    <tr>
      <td>userID</td>
      <td>String</td>
      <td>Mã định danh người dùng</td>
    </tr>
    <tr>
      <td>HovaTen</td>
      <td>String</td>
      <td>Họ tên người tham gia hệ thống</td>
    </tr>
    <tr>
      <td rowspan="2">Tài khoản</td>
      <td>NgaySinh</td>
      <td>Date</td>
      <td>Ngày sinh của người tham gia hệ thống</td>
    </tr>
    <tr>
      <td>Email</td>
      <td>String</td>
      <td>Email của người tham gia hệ thống</td>
    </tr>
    <tr>
      <td rowspan="2">Chatbot</td>
      <td>Chucvu</td>
      <td>String</td>
      <td>Chức vụ người tham gia hệ thống</td>
    </tr>
    <tr>
      <td>Tentaikhoan</td>
      <td>String</td>
      <td>Tên tài khoản của người dùng</td>
    </tr>
    <tr>
      <td></td>
      <td>Matkhau</td>
      <td>String</td>
      <td>Mật khẩu của người dùng</td>
    </tr>
    <tr>
      <td></td>
      <td>Cauhoi</td>
      <td>String</td>
      <td>Câu hỏi mà chatbot nhận được từ người dùng</td>
    </tr>
    <tr>
      <td></td>
      <td>Cautraloi</td>
      <td>String</td>
      <td>Câu trả lời mà bot sẽ trả lời dựa theo câu hỏi người dùng</td>
    </tr>
    <tr>
      <td>PDF</td>
      <td></td>
      <td></td>
      <td>Các tài liệu PDF trong hệ thống được bot dựa vào để vấn đáp với người dùng</td>
    </tr>
  </tbody>
</table>

Bảng 3.1: Bảng đặc tả sơ đồ Lớp

&lt;page_number&gt;29&lt;/page_number&gt;

---

## Page 10

Xây dựng ứng dụng học máy hỗ trợ thủ tục hành chính cho sinh viên

4.1. Bảng cơ sở dữ liệu

<table>
  <thead>
    <tr>
      <th>Tên trường</th>
      <th>Kiểu dữ liệu</th>
      <th>Cỡ dữ liệu</th>
      <th>Khuôn dạng</th>
      <th>Ràng buộc</th>
      <th>Mô tả</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ID</td>
      <td>INT</td>
      <td>10</td>
      <td>Số</td>
      <td>PRIMARY KEY, NOT NULL</td>
      <td>Mã người dùng</td>
    </tr>
    <tr>
      <td>fullname</td>
      <td>VARCHAR</td>
      <td>255</td>
      <td>Chữ</td>
      <td>NOT NULL</td>
      <td>Họ tên người dùng</td>
    </tr>
    <tr>
      <td>username</td>
      <td>VARCHAR</td>
      <td>255</td>
      <td>Chữ</td>
      <td>NOT NULL</td>
      <td>Tên đăng nhập</td>
    </tr>
    <tr>
      <td>email</td>
      <td>VARCHAR</td>
      <td>255</td>
      <td>Chữ</td>
      <td>NOT NULL</td>
      <td>Email</td>
    </tr>
    <tr>
      <td>dob</td>
      <td>DATE</td>
      <td></td>
      <td></td>
      <td>NOT NULL</td>
      <td>Ngày tháng năm sinh</td>
    </tr>
    <tr>
      <td>password</td>
      <td>VARCHAR</td>
      <td>255</td>
      <td>Chữ</td>
      <td>NOT NULL</td>
      <td>Mật khẩu</td>
    </tr>
    <tr>
      <td>Role</td>
      <td>ENUM</td>
      <td>'admin', 'gv','sv'</td>
      <td>Chữ</td>
      <td>NOT NULL</td>
      <td>Vai trò của người dùng</td>
    </tr>
  </tbody>
</table>

Bảng 3.2: Bảng dữ liệu người dùng

&lt;page_number&gt;30&lt;/page_number&gt;
