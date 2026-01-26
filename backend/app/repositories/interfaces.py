from abc import ABC, abstractmethod
from uuid import UUID


class MembershipRepository(ABC):
    @abstractmethod
    def is_member(self, user_id: UUID, project_id: UUID) -> bool:
        ...


class RoleRepository(ABC):
    @abstractmethod
    def user_has_role(
        self,
        user_id: UUID,
        role_name: str,
        project_id: UUID,
    ) -> bool:
        ...


class ApprovalRepository(ABC):
    @abstractmethod
    def is_assigned_approver(
        self,
        user_id: UUID,
        document_id: UUID,
    ) -> bool:
        ...

    @abstractmethod
    def is_current_approver(
        self,
        user_id: UUID,
        document_id: UUID,
    ) -> bool:
        ...
