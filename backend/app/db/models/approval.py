import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from app.db.mixins.base import UUIDPrimaryKeyMixin
from app.db.enums.status import ApprovalStatus

if TYPE_CHECKING:
    from app.db.models.document import Document


class ApprovalRequest(UUIDPrimaryKeyMixin, SQLModel, table=True):
    __tablename__ = "approval_requests"

    document_id: uuid.UUID = Field(
        foreign_key="documents.id", index=True, nullable=False
    )
    workflow_id: uuid.UUID = Field(
        foreign_key="workflows.id", nullable=False
    )

    status: ApprovalStatus = Field(
        default=ApprovalStatus.pending, nullable=False
    )

    submitted_by: uuid.UUID = Field(
        foreign_key="users.id", nullable=False
    )
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Relationships
    steps: List["ApprovalStep"] = Relationship(
        back_populates="approval_request"
    )
    document: "Document" = Relationship(
        back_populates="approval_requests"
    )


class ApprovalStep(UUIDPrimaryKeyMixin, SQLModel, table=True):
    __tablename__ = "approval_steps"

    approval_request_id: uuid.UUID = Field(
        foreign_key="approval_requests.id", index=True, nullable=False
    )

    step_order: int = Field(nullable=False)
    approver_id: uuid.UUID = Field(
        foreign_key="users.id", nullable=False
    )

    status: ApprovalStatus = Field(
        default=ApprovalStatus.pending, nullable=False
    )

    action_at: Optional[datetime] = None
    comment: Optional[str] = None

    # Relationships
    approval_request: "ApprovalRequest" = Relationship(
        back_populates="steps"
    )
