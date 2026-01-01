import uuid
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.db.mixins.base import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.project import Project
    from app.db.models.user import OrganizationUser



class Organization(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "organizations"

    name: str = Field(nullable=False, index=True)

    # Relationships
    members: list["OrganizationUser"] = Relationship(back_populates="organization")
    projects: list["Project"] = Relationship(back_populates="organization")
