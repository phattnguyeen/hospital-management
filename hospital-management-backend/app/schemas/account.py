from pydantic import BaseModel, Field, constr
from typing import Optional
from uuid import UUID
from datetime import datetime

# Enum for role choices to ensure valid roles
ROLE_CHOICES = ['patient', 'doctor', 'employee', 'admin']

# Schema for creating an account
class AccountCreate(BaseModel):
    password: str = Field(..., max_length=255)  # Password hash to be used
    role: str = Field(..., max_length=50, pattern="^(patient|doctor|employee|admin)$")  # Validate role directly with regex
    phone_number: str = Field(..., max_length=20)  # Unique phone number for the account
    is_verified: Optional[bool] = Field(default=False)  # Optional verification status
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)  # Automatically set creation time


# Schema for updating an account
class AccountUpdate(BaseModel):
    password_hash: Optional[str] = Field(None, max_length=255)  # Optional password hash for updating
    phone_number: Optional[str] = Field(None, max_length=20)  # Optional phone number update
    is_verified: Optional[bool]  # Optional verification status update
    role: Optional[str] = Field(None, pattern="^(patient|doctor|employee|admin)$")  # Optional role change
    patient_id: Optional[str] = Field(None, max_length=100)  # Update patient_id
    doctor_id: Optional[str] = Field(None, max_length=100)  # Update doctor_id
    employee_id: Optional[str] = Field(None, max_length=100)  # Update employee_id



# Schema for reading account data
class AccountRead(BaseModel):
    account_id: UUID
    password_hash: str
    role: str
    phone_number: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None
    employee_id: Optional[str] = None
