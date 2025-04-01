from sqlalchemy import Column, Integer, String, Text, Date, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base

# Account Table (Optimized)
class Account(Base):
    __tablename__ = "account"
    account_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid(), index=True)
    username = Column(String(50), unique=True, nullable=False)
    passwordHash = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=False)  # Unified user reference
    user_type = Column(String(50), CheckConstraint("user_type IN ('patient', 'doctor', 'employee')"))