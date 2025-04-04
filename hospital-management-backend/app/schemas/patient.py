from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional

# Define a Pydantic model for creating a patient
class PatientCreate(BaseModel):
    # patient_id: Optional[str] = Field(None, max_length=100)
    full_name: str = Field(..., max_length=100)
    birth_date: Optional[date] = Field(None)
    gender: Optional[str] = Field(None, pattern="^(Male|Female|Other)$")
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None)
    medical_history: Optional[str] = Field(None)

# Define a Pydantic model for updating a patient
class PatientUpdate(BaseModel):
    # patient_id: Optional[str] = Field(None, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)
    birth_date: Optional[date] = Field(None)
    gender: Optional[str] = Field(None, pattern="^(Male|Female|Other)$")
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None)
    medical_history: Optional[str] = Field(None)

# Define a Pydantic model for reading patient data
class PatientRead(BaseModel):
    patient_id: str
    full_name: str
    birth_date: Optional[date]
    gender: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    medical_history: Optional[str]

