
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Đọc file .env ở thư mục gốc dự án
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Lấy địa chỉ kết nối Database
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL chưa được cấu hình trong file .env")


# Khởi tạo SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)


# Tạo Session cho các thao tác Database
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Lớp cơ sở cho các ORM Model
class Base(DeclarativeBase):
    pass


# Dependency dùng trong các API FastAPI
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
