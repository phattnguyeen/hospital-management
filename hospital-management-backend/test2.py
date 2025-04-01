from sqlalchemy import (
    create_engine, Column, String, Integer, Text, Date, ForeignKey, DECIMAL, Time, CheckConstraint, event
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import text
import random
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

DATABASE_URL = "postgresql://phatnguyen:fFqMCm0RqQwdwq0rujX4IyNpHcCg8DA2@dpg-cvameh5svqrc73bvpveg-a.oregon-postgres.render.com/hospitalmanagement_txr6"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def generate_unique_id(session: Session, prefix: str, table: str, column: str):
    """Tạo ID duy nhất bằng cách thêm số ngẫu nhiên vào prefix."""
    while True:
        new_id = f"{prefix}{random.randint(10000, 99999)}"
        print(f"Generated ID: {new_id}")  # Debugging
        result = session.execute(text(f"SELECT 1 FROM {table} WHERE {column} = :id"), {"id": new_id}).fetchone()
        if not result:
            return new_id

# Bảng bệnh nhân
class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(String(100), primary_key=True)
    full_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    gender = Column(String(10), CheckConstraint("gender IN ('Male', 'Female', 'Other')"))
    address = Column(String(255))
    phone_number = Column(String(100), unique=True)
    mail = Column(String(100), unique=True)
    medical_history = Column(Text)

def before_insert_patient(mapper, connection, target):
    """Sự kiện trước khi chèn bệnh nhân để tạo ID tự động."""
    with Session(connection) as session:
        target.patient_id = generate_unique_id(session, "PAT", "patient", "patient_id")

event.listen(Patient, "before_insert", before_insert_patient)

# Hàm tạo bảng
def create_tables():
    """Tạo bảng trong cơ sở dữ liệu."""
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

# Hàm drop bảng
def drop_tables():
    """Xóa toàn bộ bảng trong cơ sở dữ liệu."""
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Tables dropped successfully!")

# Hàm test chèn dữ liệu
def test_insert_patient():
    """Kiểm tra xem bệnh nhân có được thêm đúng không."""
    with SessionLocal() as session:
        new_patient = Patient(
            full_name="John Doe",
            birth_date="1985-04-12",
            gender="Male",
            address="123 Main St, NY",
            phone_number="123-456-7890",
            mail="johndoe@example.com",
            medical_history="No known allergies"
        )
        session.add(new_patient)
        session.commit()
        print(f"🩺 New patient added with ID: {new_patient.patient_id}")

# Chạy test
if __name__ == "__main__":
    # drop_tables()  # Xóa bảng cũ (chỉ chạy khi cần reset DB)
    create_tables()  # Tạo bảng mới
    test_insert_patient()  # Kiểm tra chèn bệnh nhân
