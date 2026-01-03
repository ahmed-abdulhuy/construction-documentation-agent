from uuid import UUID
from sqlalchemy import func
from sqlmodel import Session, select

from app.repositories.interfaces import ApprovalRepository
from app.db.models.approval import ApprovalStep
from app.db.models.approval import ApprovalRequest
from app.db.enums.status import ApprovalStatus


class SQLApprovalRepository(ApprovalRepository):
    def __init__(self, session: Session):
        self.session = session

    def is_assigned_approver(
        self,
        user_id: UUID,
        document_id: UUID,
    ) -> bool:
        stmt = (
            select(ApprovalStep.id)
            .join(ApprovalRequest)
            .where(ApprovalRequest.document_id == document_id)
            .where(ApprovalStep.user_id == user_id)
            .where(ApprovalStep.status == ApprovalStatus.pending)

        )
        return self.session.exec(stmt).first() is not None

    def is_current_approver(
        self,
        user_id: UUID,
        document_id: UUID,
    ) -> bool:
        stmt = (
            select(ApprovalStep.id)
            .join(ApprovalRequest)
            .where(ApprovalRequest.document_id == document_id)
            .where(ApprovalStep.user_id == user_id)
            .where(ApprovalStep.status == ApprovalStatus.pending)
            .where(
                ApprovalStep.step_order
                == select(func.min(ApprovalStep.step_order))
                .where(ApprovalStep.approval_request_id == ApprovalRequest.id)
                .where(ApprovalStep.status == ApprovalStatus.pending)
            )
        )
        return self.session.exec(stmt).first() is not None
