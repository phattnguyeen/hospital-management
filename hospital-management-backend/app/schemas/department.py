from pydantic import BaseModel, Field
from typing import Optional

# Schema for creating a department
class DepartmentCreate(BaseModel):
    #department_id: str = Field(..., max_length=100)
    department_name: str = Field(..., max_length=100)

# Schema for updating a department
class DepartmentUpdate(BaseModel):
    #department_id: str = Field(..., max_length=100)
    department_name: Optional[str] = Field(None, max_length=100)

# Schema for reading department data
class DepartmentRead(BaseModel):
    department_id: str
    department_name: str

