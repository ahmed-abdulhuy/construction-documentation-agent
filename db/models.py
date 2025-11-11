from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from typing import List, Optional
from datetime import date
import uuid
from pydantic import field_validator, BaseModel
# from sqlalchemy import Column

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
    wirs: List["WIR"] = Relationship(back_populates="discipline")



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
    issuingDate: date = Field(default=date.today())
    drawingRef: str
    areaRef: str
    partLevelRef: Optional[str]=None
    plannedInspDate: date # planned date of inspection
    inspectionDate: date
    # Discipline foreign ID
    discipline_id: uuid.UUID = Field(foreign_key="disciplines.id")
    discipline: Optional[Discipline] = Relationship(back_populates='wirs')
    # Representation for debugging
    def __repr__(self):
        return f"<Request {self.id} by User {self.user_id}>"



class WIRCreate(BaseModel):
    title: str
    drawingRef: str
    areaRef: str
    partLevelRef: Optional[str]=None
    plannedInspDate: date # planned date of inspection
    inspectionDate: date
    # Discipline foreign ID
    discipline_id: uuid.UUID

    @field_validator('plannedInspDate', 'inspectionDate', mode='before')
    @classmethod
    def validate_dates(cls, v):
        if isinstance(v, str):
            return date.fromisoformat(v)
        return v