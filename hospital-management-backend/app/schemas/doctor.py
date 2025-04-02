from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# Schema for creating a doctor
class DoctorCreate(BaseModel):
    full_name: str = Field(..., max_length=100)
    birth_date: Optional[date] = Field(None)
    gender: Optional[str] = Field(None, pattern="^(Male|Female|Other)$")
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=100)
    national_id: Optional[str] = Field(None, max_length=100)
    experience: Optional[int] = Field(None, ge=0)  # Must be greater than or equal to 0
    department_id: Optional[str] = Field(None, max_length=100)

# Schema for updating a doctor
class DoctorUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    birth_date: Optional[date] = Field(None)
    gender: Optional[str] = Field(None, pattern="^(Male|Female|Other)$")
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=100)
    national_id: Optional[str] = Field(None, max_length=100)
    experience: Optional[int] = Field(None, ge=0)  # Must be greater than or equal to 0
    department_id: Optional[str] = Field(None, max_length=100)

# Schema for reading doctor data
class DoctorRead(BaseModel):
    doctor_id: str
    full_name: str
    birth_date: Optional[date]
    gender: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    national_id: Optional[str]
    experience: Optional[int]
    department_id: Optional[str]

    class Config:
        orm_mode = True