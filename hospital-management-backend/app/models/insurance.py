from sqlalchemy import Column, Integer, String, Text, Date, CheckConstraint,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base

class Insurance(Base):
    __tablename__ = "insurance"
    insurance_id = Column(String(100), primary_key=True)
    patient_id = Column(String(100), ForeignKey("patient.patient_id"), nullable=False)
    treatment_facility = Column(String(255))
