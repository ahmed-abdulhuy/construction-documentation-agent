import uuid
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.db.mixins.base import TimestampMixin, SoftDeleteMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.db.models.organization import Organization
    from app.db.models.role import ProjectUserRole
    from app.db.models.user import ProjectUser


class Project(UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, SQLModel, table=True):
    __tablename__ = "projects"

    organization_id: uuid.UUID = Field(foreign_key="organizations.id", index=True, nullable=False)
    name: str = Field(nullable=False, index=True)

    # Relationships
    organization: "Organization" = Relationship(back_populates="projects")
    members: list["ProjectUser"] = Relationship(back_populates="project")
    roles: list["ProjectUserRole"] = Relationship(back_populates="project")
