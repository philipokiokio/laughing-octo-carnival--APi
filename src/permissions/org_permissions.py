from fastapi import Depends, HTTPException, status

from src.auth.oauth import get_current_user
from src.organization.org_repository import org_member_repo, org_repo


def test_permission(org_slug: str, current_user: dict = Depends(get_current_user)):
    org_check = org_repo.get_org(org_slug)
    if not org_check:
        raise HTTPException(
            detail="Organization does not exists",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    org_member_check = org_member_repo.get_org_member_by_user_id(
        org_check.id, current_user.id
    )
    if not org_member_check:
        raise HTTPException(
            detail="account is not a member of this team",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return current_user
