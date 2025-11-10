from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import Column

class User(SQLModel, table=True):  # Defines a SQL table
    __tablename__ = "users"

    # UUID as primary key
    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    # User fields
    email: str = Field(unique=True)  # Email is unique
    name: str  # Full name of the user

    # Representation for debugging
    def __repr__(self):
        return f"<User {self.email}>"


class Request (SQLModel, table=True):
    __tablename__ = "requests"

    # UUID as primary key
    id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )

    # Request fields
    title: str  # The query text
    discipline: str  # The discipline of the request
    description: Optional[str] = None  # Optional description
    issuingDate: datetime  # Date of issue

    # Representation for debugging
    def __repr__(self):
        return f"<Request {self.id} by User {self.user_id}>"