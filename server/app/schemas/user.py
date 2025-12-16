from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: str = Field(..., examples=["ADMIN", "DRAFTER", "SHIFT_LEAD", "FINAL_QC"])


class UserResponse(BaseModel):
    id: UUID
    name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
