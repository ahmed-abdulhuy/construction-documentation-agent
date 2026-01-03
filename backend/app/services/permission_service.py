# services/permission_service.py

from uuid import UUID
from app.db.models.document import Document


class PermissionService:
    """
    Authoritative permission engine.
    Fail-closed by default.
    """

    # -------------------------
    # Document creation
    # -------------------------
    def can_create_document(self, user, project_id: UUID) -> bool:
        if not user.is_active:
            return False

        if not user.is_member_of(project_id):
            return False

        if not user.has_role("Engineer", project_id):
            return False

        return True

    # -------------------------
    # Read document
    # -------------------------
    def can_read_document(self, user, document: Document) -> bool:
        if not user.is_member_of(document.project_id):
            return False

        if document.created_by == user.id:
            return True

        if user.is_assigned_approver(document.id):
            return True

        # State-based visibility
        if document.status == "approved":
            return True

        return False

    # -------------------------
    # Update metadata
    # -------------------------
    def can_update_document(self, user, document: Document) -> bool:
        if document.status != "draft":
            return False

        if document.created_by != user.id:
            return False

        if not user.has_role("Engineer", document.project_id):
            return False

        return True

    # -------------------------
    # Upload new version
    # -------------------------
    def can_upload_version(self, user, document: Document) -> bool:
        if document.status not in ("draft", "rejected"):
            return False

        if document.created_by != user.id:
            return False

        if not user.has_role("Engineer", document.project_id):
            return False

        return True

    # -------------------------
    # Submit for approval
    # -------------------------
    def can_submit_document(self, user, document: Document) -> bool:
        if document.status != "draft":
            return False

        if document.created_by != user.id:
            return False

        if not document.workflow_id:
            return False

        return True

    # -------------------------
    # Approve
    # -------------------------
    def can_approve_document(self, user, document: Document) -> bool:
        if document.status != "submitted":
            return False

        if document.created_by == user.id:
            return False

        if not user.is_current_approver(document.id):
            return False

        return True

    # -------------------------
    # Reject
    # -------------------------
    def can_reject_document(self, user, document: Document) -> bool:
        # Same rules as approve
        return self.can_approve_document(user, document)

    # -------------------------
    # Comment
    # -------------------------
    def can_comment(self, user, document: Document) -> bool:
        if not user.is_member_of(document.project_id):
            return False

        return True

    # -------------------------
    # Download
    # -------------------------
    def can_download_document(self, user, document: Document) -> bool:
        if document.status != "approved":
            return False

        if not user.is_member_of(document.project_id):
            return False

        return True
