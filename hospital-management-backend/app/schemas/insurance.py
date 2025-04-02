from pydantic import BaseModel, Field
from typing import Optional

# Schema for creating an insurance record
class InsuranceCreate(BaseModel):
    insurance_id: str = Field(..., max_length=100)
    patient_id: str = Field(..., max_length=100)
    treatment_facility: Optional[str] = Field(None, max_length=255)

# Schema for updating an insurance record
class InsuranceUpdate(BaseModel):
    insurance_id: str = Field(..., max_length=100)
    patient_id: Optional[str] = Field(None, max_length=100)
    treatment_facility: Optional[str] = Field(None, max_length=255)

# Schema for reading insurance data
class InsuranceRead(BaseModel):
    insurance_id: str
    patient_id: str
    treatment_facility: Optional[str]

    class Config:
        orm_mode = True