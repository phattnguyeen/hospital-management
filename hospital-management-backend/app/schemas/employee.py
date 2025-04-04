from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# Schema for creating an employee
class EmployeeCreate(BaseModel):
    full_name: str = Field(..., max_length=100)
    birth_date: Optional[date] = Field(None)
    gender: Optional[str] = Field(None, pattern="^(Male|Female|Other)$")
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=100)
    position: str = Field(..., max_length=50)
    department_id: Optional[str] = Field(None, max_length=100)

# Schema for updating an employee
class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=100)
    birth_date: Optional[date] = Field(None)
    gender: Optional[str] = Field(None, pattern="^(Male|Female|Other)$")
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=100)
    position: Optional[str] = Field(None, max_length=50)
    department_id: Optional[str] = Field(None, max_length=100)

# Schema for reading employee data
class EmployeeRead(BaseModel):
    employee_id: str
    full_name: str
    birth_date: Optional[date]
    gender: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    position: str
    department_id: Optional[str]

