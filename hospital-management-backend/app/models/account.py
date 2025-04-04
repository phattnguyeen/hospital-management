from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base

class Account(Base):
    __tablename__ = "account"
    
    account_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid(), index=True)
    # username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  
    otp = Column(String(6), nullable=True)  # Thêm trường OTP
    role = Column(String(50), nullable=True)
    user_id = Column(String(100), nullable=True)  # Có thể NULL ban đầu, cập nhật sau khi nhập thông tin
    phone_number = Column(String(20), unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)  
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())