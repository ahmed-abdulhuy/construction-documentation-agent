import uuid
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.db.mixins.base import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.project import Project
    from app.db.models.user import User


class Role(UUIDPrimaryKeyMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "roles"

    name: str = Field(nullable=False, index=True)

    # Relationships
    assignments: list["ProjectUserRole"] = Relationship(back_populates="role")


class ProjectUserRole(SQLModel, TimestampMixin, table=True):
    __tablename__ = "project_user_roles"

    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True, nullable=False)
    project_id: uuid.UUID = Field(foreign_key="projects.id", primary_key=True, nullable=False)
    role_id: uuid.UUID = Field(foreign_key="roles.id", primary_key=True, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="roles")
    project: "Project" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="assignments")
