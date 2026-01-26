from uuid import UUID

class UserContext:
    def __init__(
        self,
        *,
        user_id: UUID,
        is_active: bool,
        is_superuser: bool,
        membership_repo,
        role_repo,
        approval_repo,
    ):
        self.id = user_id
        self.is_active = is_active
        self.is_superuser = is_superuser

        self._membership_repo = membership_repo
        self._role_repo = role_repo
        self._approval_repo = approval_repo

    def is_member_of(self, project_id: UUID) -> bool:
        if self.is_superuser:
            return True
        return self._membership_repo.is_member(self.id, project_id)

    def has_role(self, role_name: str, project_id: UUID) -> bool:
        if self.is_superuser:
            return True
        return self._role_repo.user_has_role(
            self.id, role_name, project_id
        )

    def is_assigned_approver(self, document_id: UUID) -> bool:
        return self._approval_repo.is_assigned_approver(
            self.id, document_id
        )

    def is_current_approver(self, document_id: UUID) -> bool:
        return self._approval_repo.is_current_approver(
            self.id, document_id
        )
