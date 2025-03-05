# schemas/auth.py

from pydantic import BaseModel

class Token(BaseModel):
    """Schema for the authentication token response."""
    access_token: str
    token_type: str
