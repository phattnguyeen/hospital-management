from sqlalchemy import Column, Integer, String, Text, Date, CheckConstraint,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base

class Department(Base):
    __tablename__ = "department"
    department_id = Column(String(100), primary_key=True, server_default="gen_department_id()")
    department_name = Column(String(100), nullable=False)