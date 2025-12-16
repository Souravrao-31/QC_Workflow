from fastapi import Depends, HTTPException, status
from typing import Iterable

from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.enums import UserRole


def require_roles(*allowed_roles: UserRole):

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not allowed for this action",
            )
        return current_user

    return role_checker
