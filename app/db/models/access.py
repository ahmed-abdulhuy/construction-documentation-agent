import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field
from app.db.mixins.base import UUIDPrimaryKeyMixin


#* Only introduce this after role/workflow logic proves insufficient.
class DocumentAccess(UUIDPrimaryKeyMixin, SQLModel, table=True):
    """
    Explicit per-user access override.
    Use ONLY when RBAC/workflows are insufficient.
    """
    __tablename__ = "document_access"

    document_id: uuid.UUID = Field(
        foreign_key="documents.id", index=True, nullable=False
    )
    user_id: uuid.UUID = Field(
        foreign_key="users.id", nullable=False
    )

    can_read: bool = Field(default=True)
    can_edit: bool = Field(default=False)
    can_approve: bool = Field(default=False)

    granted_at: datetime = Field(default_factory=datetime.utcnow)
