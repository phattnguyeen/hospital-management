from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

# Schema for creating an account
class AccountCreate(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., max_length=100)
    role: str = Field(..., max_length=100)
    user_id: str = Field(..., max_length=100)
    user_type: str = Field(..., pattern="^(patient|doctor|employee)$")

# Schema for updating an account
class AccountUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    password: Optional[str] = Field(None, max_length=100)
    role: Optional[str] = Field(None, max_length=100)
    user_id: Optional[str] = Field(None, max_length=100)
    user_type: Optional[str] = Field(None, pattern="^(patient|doctor|employee)$")

# Schema for reading account data
class AccountRead(BaseModel):
    account_id: UUID
    username: str
    role: str
    user_id: str
    user_type: str

    class Config:
        orm_mode = True