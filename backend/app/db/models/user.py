import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.db.mixins.base import TimestampMixin, SoftDeleteMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.organization import Organization
    from app.db.models.project import Project
    from app.db.models.role import ProjectUserRole

# -------------------------
# User
# -------------------------
class User(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, SQLModel, table=True):
    __tablename__ = "users"

    email: str = Field(index=True, nullable=False, unique=True)
    full_name: str = Field(nullable=False)
    hashed_password: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)

    # Relationships
    organizations: list["OrganizationUser"] = Relationship(back_populates="user")
    projects: list["ProjectUser"] = Relationship(back_populates="user")
    roles: list["ProjectUserRole"] = Relationship(back_populates="user")


# -------------------------
# Organization User (membership)
# -------------------------
class OrganizationUser(SQLModel, TimestampMixin, table=True):
    __tablename__ = "organization_users"

    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True, nullable=False)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id", primary_key=True, nullable=False)
    is_org_admin: bool = Field(default=False, nullable=False)
    joined_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="organizations")
    organization: "Organization" = Relationship(back_populates="members")


# -------------------------
# Project User (membership)
# -------------------------
class ProjectUser(SQLModel, TimestampMixin, table=True):
    __tablename__ = "project_users"

    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True, nullable=False)
    project_id: uuid.UUID = Field(foreign_key="projects.id", primary_key=True, nullable=False)
    joined_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="projects")
    project: "Project" = Relationship(back_populates="members")
