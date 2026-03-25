from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class RegisterSchema(BaseModel):
    email : EmailStr
    password: str = Field(min_length=6)
    role: Literal["free", "paid"] = "free"

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponseSchema(BaseModel):
    access_token: str