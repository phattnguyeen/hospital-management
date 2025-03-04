from sqlalchemy import Column, Integer, String, Text, Date, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class Patient(Base):
    __tablename__ = "patient"

    patient_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid(), index=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password = Column(Text, nullable=False)
    age = Column(Integer, CheckConstraint("age >= 0"))
    phone_no = Column(String(15), unique=True)
    address = Column(Text)
    patient_type = Column(String(50))
    sex = Column(String(10), CheckConstraint("sex IN ('Male', 'Female', 'Other')"))
    admit_date = Column(Date)
    discharge_date = Column(Date, CheckConstraint("discharge_date IS NULL OR discharge_date >= admit_date"))