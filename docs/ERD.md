# ERD - Lab Booking System

## 1. Sơ đồ cơ sở dữ liệu

```mermaid
erDiagram
    USERS ||--o{ BOOKINGS : creates
    ROOMS ||--o{ BOOKINGS : receives
    BOOKINGS ||--o{ BOOKING_EQUIPMENT : includes
    EQUIPMENT ||--o{ BOOKING_EQUIPMENT : registered
    BOOKING_EQUIPMENT ||--o{ LOANS : generates
    LOANS ||--o{ DAMAGE_REPORTS : records
    USERS ||--o{ DAMAGE_REPORTS : reports

    USERS {
        int id PK
        varchar full_name
        varchar email UK
        varchar password_hash
        varchar role
        timestamp created_at
    }

    ROOMS {
        int id PK
        varchar name
        varchar location
        int capacity
        text description
        boolean is_active
    }

    EQUIPMENT {
        int id PK
        varchar name
        varchar asset_code UK
        varchar description
        varchar status
    }

    BOOKINGS {
        int id PK
        int user_id FK
        int room_id FK
        timestamp start_time
        timestamp end_time
        varchar purpose
        varchar status
        timestamp created_at
    }

    BOOKING_EQUIPMENT {
        int id PK
        int booking_id FK
        int equipment_id FK
        int quantity
    }

    LOANS {
        int id PK
        int booking_equipment_id FK
        timestamp checkout_at
        timestamp return_at
        varchar condition_on_return
        varchar status
    }

    DAMAGE_REPORTS {
        int id PK
        int loan_id FK
        int reporter_id FK
        text description
        varchar image_path
        timestamp reported_at
        varchar status
    }
```

## 2. Mô tả quan hệ

- Một người dùng có thể tạo nhiều yêu cầu đặt lịch.
- Một phòng có thể xuất hiện trong nhiều yêu cầu đặt lịch.
- Một yêu cầu đặt lịch có thể đăng ký nhiều thiết bị.
- Một thiết bị có thể xuất hiện trong nhiều yêu cầu đặt lịch.
- Một mục thiết bị trong yêu cầu đặt lịch có thể phát sinh nhiều lần mượn/trả.
- Một lần mượn/trả có thể có nhiều báo cáo hư hỏng.
- Một người dùng có thể lập nhiều báo cáo hư hỏng.

## 3. Quy tắc dữ liệu

- Email người dùng phải duy nhất.
- Mã tài sản thiết bị phải duy nhất.
- Thời gian kết thúc phải sau thời gian bắt đầu.
- Số lượng thiết bị phải lớn hơn 0.
- Chỉ yêu cầu được duyệt mới được mượn thiết bị.
- Không cho phép hai lịch đặt cùng phòng bị chồng lấn thời gian.

## 4. Các bảng trong hệ thống

| STT | Tên bảng | Chức năng |
|---|---|---|
| 1 | USERS | Lưu thông tin người dùng và vai trò |
| 2 | ROOMS | Quản lý phòng thực hành |
| 3 | EQUIPMENT | Quản lý thiết bị |
| 4 | BOOKINGS | Lưu yêu cầu đặt phòng |
| 5 | BOOKING_EQUIPMENT | Lưu thiết bị được đăng ký trong từng yêu cầu |
| 6 | LOANS | Quản lý quá trình mượn và trả thiết bị |
| 7 | DAMAGE_REPORTS | Lưu báo cáo thiết bị hư hỏng |

## 5. Kết luận

Cơ sở dữ liệu Lab Booking System gồm 7 bảng chính, hỗ trợ quản lý người dùng, phòng thực hành, thiết bị, yêu cầu đặt lịch, mượn trả và báo cáo hư hỏng.

Thiết kế sử dụng khóa chính (PK), khóa ngoại (FK), quan hệ một-nhiều (1:N) và bảng trung gian để quản lý quan hệ nhiều-nhiều (N:N) giữa yêu cầu đặt lịch và thiết bị.