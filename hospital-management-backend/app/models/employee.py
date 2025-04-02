from sqlalchemy import Column, Integer, String, Text, Date, CheckConstraint,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base


class Employee(Base):
    __tablename__ = "employee"
    employee_id = Column(String(100), primary_key=True, server_default="gen_employee_id()")
    full_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    gender = Column(String(10), CheckConstraint("gender IN ('Male', 'Female', 'Other')"))
    address = Column(String(255))
    phone_number = Column(String(100), unique=True)
    position = Column(String(50), nullable=False)
    department_id = Column(String(100), ForeignKey("department.department_id"), nullable=True)
