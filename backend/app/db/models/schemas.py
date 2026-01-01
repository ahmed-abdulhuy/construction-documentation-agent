from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import uuid
from datetime import date


# ----------------------
# Token Schemas
# ----------------------
class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ----------------------
# User Schemas
# ----------------------
class UserBase(BaseModel):
    email: EmailStr
    fullname: str
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)

class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)

class UserRegister(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    name: str | None = Field(default=None, max_length=255)

class UserPublic(UserBase):
    id: uuid.UUID

class UsersPublic(BaseModel):
    data: List[UserPublic]
    count: int

# Generic message
class Message(BaseModel):
    message: str


# ----------------------
# WIR Schemas
# ----------------------
class WIRCreate(BaseModel):
    title: str
    description: str
    category: str
    priority: str
    status: str = "Draft"

class WIRRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    category: str
    priority: str
    status: str
    created_by: uuid.UUID
    issuing_date: date
    updated_at: Optional[date]
    submitted_at: Optional[date]
