from sqlalchemy import Column, Integer, String, Text, Date, CheckConstraint,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base

class Doctor(Base):
    __tablename__ = "doctor"
    doctor_id = Column(String(100), primary_key=True, server_default="gen_doctor_id()")
    full_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    gender = Column(String(10), CheckConstraint("gender IN ('Male', 'Female', 'Other')"))
    address = Column(String(255))
    phone_number = Column(String(20), ForeignKey("account.phone_number"), unique=True, nullable=False)
    national_id = Column(String(100), unique=True)
    experience = Column(Integer, CheckConstraint("experience >= 0"))
    department_id = Column(String(100), ForeignKey("department.department_id"), nullable=True)