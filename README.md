# LAB BOOKING SYSTEM
## Hệ thống đặt lịch phòng thực hành và thiết bị

### 1. Giới thiệu
Dự án xây dựng hệ thống đặt lịch phòng thực hành và thiết bị trong trường học.
Hệ thống giúp giảng viên, sinh viên và nhân viên phòng thực hành quản lý
việc đặt phòng, đăng ký thiết bị, mượn và trả thiết bị.

### 2. Thành viên nhóm

| STT | Họ và tên | MSSV | Vai trò |
|---|---|---|---|
| 1 | Tô Quang Thắng | 2412111038 | Trưởng nhóm - Backend, Database, triển khai |
| 2 | Vũ Đình Lâm | 2312101025 | Backend nghiệp vụ, kiểm thử API |
| 3 | Phí Trường Khánh | 2412111019 | Frontend, giao diện người dùng |

### 3. Chức năng chính
- Quản lý phòng thực hành.
- Quản lý thiết bị.
- Xem lịch phòng và thiết bị theo tuần.
- Đăng ký đặt phòng và thiết bị.
- Kiểm tra và ngăn chặn lịch đặt trùng.
- Nhân viên phòng thực hành duyệt yêu cầu đặt lịch.
- Giảng viên được ưu tiên theo quy định của đề tài.
- Quản lý quá trình mượn và trả thiết bị.
- Ghi nhận tình trạng thiết bị và báo cáo hư hỏng.
- Thống kê tình hình sử dụng phòng thực hành.

### 4. Công nghệ dự kiến
- Backend: Python, FastAPI.
- Frontend: HTML, CSS, JavaScript.
- Database: PostgreSQL.
- ORM: SQLAlchemy.
- Database Migration: Alembic.
- Authentication: JWT.
- API Documentation: Swagger / OpenAPI.
- Testing: Pytest, Postman.
- Deployment: Docker, Docker Compose, Nginx.
- CI: GitHub Actions.

### 5. Phân công công việc

**Tô Quang Thắng - Trưởng nhóm**
- Quản lý repository và tiến độ.
- Thiết kế cơ sở dữ liệu.
- Xây dựng API nền tảng, xác thực và phân quyền.
- Quản lý phòng và thiết bị.
- Docker, Nginx và CI/CD.

**Vũ Đình Lâm**
- Xây dựng nghiệp vụ đặt lịch.
- Kiểm tra lịch trùng và xử lý ưu tiên giảng viên.
- Duyệt yêu cầu đặt lịch.
- Quản lý mượn, trả và báo cáo hư hỏng.
- Kiểm thử API.

**Phí Trường Khánh**
- Thiết kế giao diện người dùng.
- Xây dựng trang đăng nhập và trang tổng quan.
- Xây dựng lịch phòng theo tuần.
- Xây dựng giao diện đặt lịch và quản lý thiết bị.
- Kết nối Frontend với Backend.

### 6. Trạng thái dự án
- [x] Tạo repository GitHub.
- [x] Khởi tạo cấu trúc thư mục.
- [ ] Xây dựng cơ sở dữ liệu.
- [ ] Xây dựng REST API.
- [ ] Xây dựng giao diện.
- [ ] Kiểm thử.
- [ ] Docker và triển khai.
- [ ] Hoàn thiện báo cáo và slide.
