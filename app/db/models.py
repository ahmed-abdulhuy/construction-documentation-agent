from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from pydantic import BaseModel, field_validator, EmailStr
from typing import List, Optional
from datetime import date
import uuid


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None


class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Generic message
class Message(SQLModel):
    message: str

# Create common BaseModel for user's shared properties
class UserBase(SQLModel):
    # User fields
    email: EmailStr = Field(unique=True)  # Email is unique
    name: str  # Full name of the user
    is_active: bool = True
    is_superuser: bool = False

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserUpdateMe(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

    


# Users table
class User(UserBase, table=True):
    __tablename__ = "users"
    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    hashed_password: str
    wirs: List["WIR"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "[WIR.createdBy]"}
        )
    # reviews: List["WIR"] = Relationship(
    #     back_populates="reviewer",
    #     sa_relationship_kwargs={"foreign_keys": "[WIR.reviewedBy]"})
    # Representation for debugging
    def __repr__(self):
        return f"<User {self.email}>"



class Discipline(SQLModel, table=True):
    __tablename__ = "disciplines"

    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    name: str
    # description: Optional[str] = None
    # wirs: List["WIR"] = Relationship(back_populates="discipline")



class WIR (SQLModel, table=True):
    __tablename__ = "wirs"

    # UUID as primary key
    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )

    title: str
    description: str
    category: str
    priority: str
    status: str

    createdBy: uuid.UUID = Field(foreign_key="users.id")

    issuingDate: date = Field(default_factory=date.today)
    updatedAt: Optional[date]=None
    submittedAt: Optional[date]=None
    # reviewedAt: Optional[date]=None

    # reviewedBy: Optional[uuid.UUID]= Field(
    #     default=None, 
    #     foreign_key="users.id",
    #     nullable=True
    #     )
    
    # reviewerComments: Optional[str]=None
    # Relationship to creator and reviewer
    creator: Optional[User] = Relationship(
        back_populates="wirs",
        sa_relationship_kwargs={"foreign_keys": "[WIR.createdBy]"}
        )
    
    # reviewer: Optional[User] = Relationship(
    #     back_populates="reviews",
    #     sa_relationship_kwargs={"foreign_keys": "[WIR.reviewedBy]"}
    #     )

    def __repr__(self):
        return f"<Request {self.id} by User {self.createdBy}>"



class WIRCreate(BaseModel):
    title: str
    description: str
    category: str
    priority: str
    status: str = "Draft"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"