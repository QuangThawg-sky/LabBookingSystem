
from sqlalchemy import select

from app.database import SessionLocal
from app.models import User, Room, Equipment
from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()


def seed_data():
    db = SessionLocal()

    try:
        # Tạo tài khoản mẫu
        users = [
            {
                "full_name": "Sinh Vien Demo",
                "email": "student@labbooking.com",
                "password": "Student@123",
                "role": "student",
            },
            {
                "full_name": "Giang Vien Demo",
                "email": "lecturer@labbooking.com",
                "password": "Lecturer@123",
                "role": "lecturer",
            },
            {
                "full_name": "Nhan Vien Demo",
                "email": "staff@labbooking.com",
                "password": "Staff@123",
                "role": "staff",
            },
        ]

        for item in users:
            existing = db.scalar(
                select(User).where(User.email == item["email"])
            )

            if existing is None:
                db.add(
                    User(
                        full_name=item["full_name"],
                        email=item["email"],
                        password_hash=password_hasher.hash(
                            item["password"]
                        ),
                        role=item["role"],
                    )
                )

        # Tạo phòng thực hành
        rooms = [
            {
                "name": "LAB-A101",
                "location": "Tang 1 - Day A",
                "capacity": 40,
                "description": "Phong thuc hanh may tinh",
            },
            {
                "name": "LAB-A102",
                "location": "Tang 1 - Day A",
                "capacity": 30,
                "description": "Phong thuc hanh lap trinh",
            },
            {
                "name": "LAB-B201",
                "location": "Tang 2 - Day B",
                "capacity": 35,
                "description": "Phong thuc hanh mang",
            },
        ]

        for item in rooms:
            existing = db.scalar(
                select(Room).where(Room.name == item["name"])
            )

            if existing is None:
                db.add(Room(**item))

        # Tạo thiết bị
        equipment_items = [
            ("Laptop Dell", "EQ001", "Laptop thuc hanh"),
            ("May chieu Epson", "EQ002", "May chieu"),
            ("Router Cisco", "EQ003", "Thiet bi mang"),
            ("Switch Cisco", "EQ004", "Bo chia mang"),
            ("Microphone", "EQ005", "Micro phong hoc"),
        ]

        for name, asset_code, description in equipment_items:
            existing = db.scalar(
                select(Equipment).where(
                    Equipment.asset_code == asset_code
                )
            )

            if existing is None:
                db.add(
                    Equipment(
                        name=name,
                        asset_code=asset_code,
                        description=description,
                        status="available",
                    )
                )

        db.commit()
        print("Da them du lieu mau thanh cong!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
