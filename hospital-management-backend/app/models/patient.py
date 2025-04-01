from sqlalchemy import Column, Integer, String, Text, Date, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base

# Patient Table
class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(String(100), primary_key=True)
    full_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    gender = Column(String(10), CheckConstraint("gender IN ('Male', 'Female', 'Other')"))
    address = Column(String(255))
    phone_number = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    medical_history = Column(Text)