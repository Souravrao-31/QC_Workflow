
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(
        default="bearer",
        description="Authentication scheme",
        examples=["bearer"],
    )


class LoginRequest(BaseModel):
    name: str
    password: str
