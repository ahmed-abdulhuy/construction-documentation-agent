import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.db.mixins.base import UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.db.enums.status import DocumentStatus
    from app.db.models.approval import ApprovalRequest


class Document(
    UUIDPrimaryKeyMixin,
    TimestampMixin,
    SoftDeleteMixin,
    SQLModel,
    table=True,
):
    __tablename__ = "documents"

    project_id: uuid.UUID = Field(
        foreign_key="projects.id", index=True, nullable=False
    )
    created_by: uuid.UUID = Field(
        foreign_key="users.id", index=True, nullable=False
    )
    workflow_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="workflows.id"
    )

    title: str = Field(nullable=False)
    description: Optional[str] = None

    status: DocumentStatus = Field(
        default=DocumentStatus.draft, nullable=False
    )

    current_version: int = Field(default=1, nullable=False)
    document_type: Optional[str] = Field(default=None)

    # Relationships
    versions: List["DocumentVersion"] = Relationship(
        back_populates="document"
    )
    comments: List["DocumentComment"] = Relationship(
        back_populates="document"
    )
    approval_requests: List["ApprovalRequest"] = Relationship(
        back_populates="document"
    )


class DocumentVersion(UUIDPrimaryKeyMixin, SQLModel, table=True):
    __tablename__ = "document_versions"

    document_id: uuid.UUID = Field(
        foreign_key="documents.id", index=True, nullable=False
    )

    version_number: int = Field(nullable=False)
    file_path: str = Field(nullable=False)

    uploaded_by: uuid.UUID = Field(
        foreign_key="users.id", nullable=False
    )
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    comment: Optional[str] = None
    is_final: bool = Field(default=False)

    # Relationships
    document: "Document" = Relationship(
        back_populates="versions"
    )


class DocumentComment(UUIDPrimaryKeyMixin, SQLModel, table=True):
    __tablename__ = "document_comments"

    document_id: uuid.UUID = Field(
        foreign_key="documents.id", index=True, nullable=False
    )
    user_id: uuid.UUID = Field(
        foreign_key="users.id", nullable=False
    )

    comment: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    document: "Document" = Relationship(
        back_populates="comments"
    )
