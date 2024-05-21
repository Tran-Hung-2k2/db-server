import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Đọc giá trị từ biến môi trường hoặc sử dụng giá trị mặc định nếu không có
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "postgres")

# Tạo URL kết nối từ các giá trị đã đọc
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo engine và sessionmaker từ URL kết nối
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency để nhận session từ pool
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
