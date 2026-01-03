from uuid import UUID
from sqlmodel import Session, select

from app.repositories.interfaces import RoleRepository
from app.db.models.role import ProjectUserRole
from app.db.models.role import Role


class SQLRoleRepository(RoleRepository):
    def __init__(self, session: Session):
        self.session = session

    def user_has_role(
        self,
        user_id: UUID,
        role_name: str,
        project_id: UUID,
    ) -> bool:
        stmt = (
            select(ProjectUserRole.user_id)
            .join(Role, Role.id == ProjectUserRole.role_id)
            .where(ProjectUserRole.user_id == user_id)
            .where(ProjectUserRole.project_id == project_id)
            .where(Role.name == role_name)
        )
        return self.session.exec(stmt).first() is not None
