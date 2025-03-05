# schemas/patient.py

from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date
from typing import Optional

# Define a Pydantic model for request validation
class PatientCreate(BaseModel):
    username: str = Field(...)
    name: str = Field(...)
    age: int = Field(..., ge=0)
    password: str = Field(...)
    phone_no: str = Field(None)
    address: str = Field(None)
    patient_type: str = Field(None)
    sex: str = Field(None)
    admit_date: date = Field(None)
    discharge_date: date = Field(None)

class PatientUpdate(BaseModel):
    username: str = Field(None)
    name: str = Field(None)
    age: int = Field(None, ge=0)
    password: str = Field(None, min_length=6)
    phone_no: str = Field(None)
    address: str = Field(None)
    patient_type: str = Field(None)
    sex: str = Field(None)
    admit_date: date = Field(None)
    discharge_date: date = Field(None)

# Pydantic model for token response
class Token(BaseModel):
    access_token: str
    token_type: str
