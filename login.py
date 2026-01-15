from pydantic import BaseModel, Field, field_validator
import re

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('username')
    def validate_username(self, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v.strip()

    @field_validator('password')
    def validate_password(self, v):
        if not v.strip():
            raise ValueError('Password cannot be empty or whitespace only')
        return v