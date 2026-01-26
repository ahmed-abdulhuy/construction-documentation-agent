from uuid import UUID
from sqlmodel import Session, select

from app.repositories.interfaces import MembershipRepository
from app.db.models.user import ProjectUser


class SQLMembershipRepository(MembershipRepository):
    def __init__(self, session: Session):
        self.session = session

    def is_member(self, user_id: UUID, project_id: UUID) -> bool:
        stmt = (
            select(ProjectUser.user_id)
            .where(ProjectUser.user_id == user_id)
            .where(ProjectUser.project_id == project_id)
        )
        return self.session.exec(stmt).first() is not None
