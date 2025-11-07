README — PHÂN TÍCH CHI TIẾT CÁC DIAGRAM
Đề tài: Web App Truyền Thông Khách Sạn (Hotel Media WebApp)

Mục đích của file:
- Giải thích, phân tích và liên hệ giữa các diagram UML đã tạo.
- Là phần “Phân tích & Thiết kế hệ thống”.

Cấu trúc thư mục (đã chuẩn):
/hotel-media-webapp
   /Activity
       ACTIVITY DIAGRAM — (1) SOCIAL LOGIN OAUTH.png
       ACTIVITY DIAGRAM — (2) ADMIN TẠO BÀI VIẾT (DRAFT).png
       ACTIVITY DIAGRAM — (3) PUBLISH ĐA KÊNH (WEB,FB,TIKTOK,ZALO,YOUTUBE).png
       ACTIVITY DIAGRAM — (4) USER COMMENT.png
       ACTIVITY DIAGRAM — (5) ADMIN DUYỆT BÌNH LUẬN.png
       activity_description.txt
   /ERD
       ERD (Database ER Diagram).png
       ERD_description.txt
   /Sequence
       SEQUENCE DIAGRAM — (1) Social Login (Google, FB , Zalo, Tiktok).png
       SEQUENCE DIAGRAM — (2) Admin Login CMS.png
       SEQUENCE DIAGRAM — (3) Create Post (Upload + Save Draft).png
       SEQUENCE DIAGRAM — (4) Publish Post đa kênh (Web + FB + TikTok + Zalo + YouTube).png
       SEQUENCE DIAGRAM — (5) Upload Media vào thư viện (MediaPage).png
       SEQUENCE DIAGRAM — (6) User xem bài viết + bình luận.png
       SEQUENCE DIAGRAM — (7) Admin duyệt bình luận.png
       SQ_description.txt
   /Use Case
       Use Case Diagram.png
       UC_description.txt
   README_diagram.txt   <-- 
------------------------------------------------------------
I. ACTORS 
------------------------------------------------------------
Danh sách actors 
1. **Viewer / Public User** — người dùng truy cập trang công khai, xem bài, bình luận.
2. **Editor** — người làm nội dung/marketing, tạo & chỉnh sửa bài, upload media, có thể livestream.
3. **Admin** — quản trị viên hệ thống, phân quyền, xuất bản đa kênh, duyệt bình luận.
4. **Social Auth Provider (Google / Facebook / Zalo / TikTok)** — hệ thống ngoại vi cung cấp OAuth2 cho đăng nhập.

------------------------------------------------------------
II. MỤC TIÊU CỦA CÁC DIAGRAM (TỔNG QUAN)
------------------------------------------------------------
- **Use Case Diagram**: Xác định phạm vi chức năng và actor liên quan.
- **Activity Diagrams (5 file)**: Mô tả luồng nghiệp vụ (social login, tạo bài, publish đa kênh, comment, duyệt comment).
- **Sequence Diagrams (7 file)**: Mô tả chi tiết tương tác tin nhắn/gọi API giữa frontend ↔ backend ↔ external services cho từng nghiệp vụ.
- **ERD**: Thiết kế mô hình dữ liệu (Users, Posts, Media, Comments, PublishStatus/Jobs, Campaigns, Analytics).

------------------------------------------------------------
III. PHÂN TÍCH TỪNG NHÓM DIAGRAM (DỰA TRÊN FILE PNG HIỆN CÓ)
------------------------------------------------------------

A. USE CASE
- File: `/Use Case/Use Case Diagram.png` (mô tả trong `/Use Case/UC_description.txt`)
- Nội dung chính: các use case như Social Login, Create/Edit Post, Upload Media, Schedule/Publish, Livestream, Comment & Moderation, Analytics, User Management.
- Ghi chú: Actors là 4 mục liệt kê ở phần I; social providers đặt là external actor (OAuth).

B. ACTIVITY DIAGRAMS
- Folder: `/Activity`
- 5 diagram tương ứng:
  1. **SOCIAL LOGIN OAUTH** — luồng từ user chọn provider → redirect OAuth → nhận token → tạo session. (Có error state “Login failed”)
  2. **ADMIN TẠO BÀI VIẾT (DRAFT)** — upload media → nhập content → lưu draft.
  3. **PUBLISH ĐA KÊNH** — Admin nhấn Publish → hệ thống gọi API các nền tảng; dùng fork/parallel trong diagram để biểu diễn calls chạy song song. (Có error case khi TikTok API fail)
  4. **USER COMMENT** — User gửi comment → lưu comment.status = pending.
  5. **ADMIN DUYỆT BÌNH LUẬN** — Admin approve/reject → update DB.

- Mối liên hệ: Activity biểu diễn “hành động” của các actors; mỗi action mapping trực tiếp đến một hoặc nhiều sequence diagram (tức Activity → Sequence).

C. SEQUENCE DIAGRAMS
- Folder: `/Sequence`
- 7 files, tương ứng flows:
  1. **Social Login (Google, FB, Zalo, TikTok)** — ghi rõ exchange OAuth code/token, kiểm tra/tao user trong DB, trả session.
  2. **Admin Login CMS** — username/password auth flow.
  3. **Create Post (Upload + Save Draft)** — upload media trước khi insert post metadata.
  4. **Publish Post đa kênh** — PublishPage → PostService → (parallel) external APIs (FB/TikTok/Zalo/YT) → update PublishStatus.
  5. **Upload Media (MediaPage)** — file upload → storage (S3) → write media record.
  6. **User xem bài viết + bình luận** — GET post data, POST comment (pending).
  7. **Admin duyệt bình luận** — GET pending comments → Approve/Reject → update.

- Ghi chú lỗi liên quan:
  - OAuth error (Sequence 1) → frontend nhận lỗi, chuyển sang Login Error UI.
  - TikTok API fail (Sequence 4) → Publish flow vẫn tiếp tục; PublishStatus cho TikTok = failed, hiển thị chi tiết kết quả cho admin.

D. ERD (Database)
- File: `/ERD/ERD (Database ER Diagram).png` (mô tả trong `/ERD/ERD_description.txt`)
- Bảng chính: `Users`, `Roles`, `Posts`, `MediaLibrary`, `Comments`, `PublicationJobs/PublishStatus`, `Campaigns`, `Analytics`
- Key points:
  - Mối quan hệ 1-n: Users → Posts, Posts → Media, Posts → Comments, Campaigns → Posts, Posts → PublicationJobs.
  - `PublicationJobs` lưu trạng thái per-channel (FB/TikTok/Zalo/YT) để tracking từng kênh.

------------------------------------------------------------
IV. ERROR CASES (THEO YÊU CẦU) — VỊ TRÍ UI & HÀNH VI
------------------------------------------------------------
1. **Login failed**  
   - Vị trí: màn hình đăng nhập (Frontend).  
   - Khi xảy ra: OAuth flow trả error (user từ chối quyền, token invalid, hoặc provider trả lỗi).  
   - Hành vi UI: hiển thị modal/toast: `"Đăng nhập không thành công. Vui lòng thử lại hoặc dùng phương thức khác."` + nút `Thử lại` / `Đóng`.

2. **TikTok API publish failed**  
   - Vị trí: trang PublishPage / Publish result modal trong Admin CMS.  
   - Khi xảy ra: backend gọi TikTok API trả lỗi (timeout, permission denied, private video, v.v.).  
   - Hành vi UI: hiển thị chi tiết kết quả publish theo kênh (ví dụ: FB: success, YT: success, TikTok: failed) + nút `Retry TikTok` và link `Xem log` (log lưu trong `PublicationJobs`).

3. **Camera không bật được (livestream)**  
   - Vị trí: trang LivestreamPage / popup permission.  
   - Khi xảy ra: trình duyệt từ chối quyền camera/mic hoặc không có thiết bị.  
   - Hành vi UI: show modal `"Không thể truy cập camera. Vui lòng kiểm tra quyền trình duyệt hoặc thiết bị."` + hướng dẫn nhanh bật quyền và nút `Thử lại`.

> Tất cả three cases chỉ là **UI error states** (thiết kế trên Figma). Backend vẫn có thể trả lỗi tương ứng, 
------------------------------------------------------------
