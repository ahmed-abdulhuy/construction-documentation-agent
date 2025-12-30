from typing import Optional
from datetime import datetime
from sqlmodel import Field, Column, func
from uuid import UUID, uuid4

class UUIDPrimaryKeyMixin:
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)


class SoftDeleteMixin:
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)


class TimestampMixin:
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

