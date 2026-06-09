from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app.api.dependencies.auth import CurrentUser
from app.db.database import get_session
from app.models.db_models import AdminUser
from app.repositories.admin_repo import get_active_admin_user


def require_admin_user(current_user: CurrentUser, session: Annotated[Session, Depends(get_session)]) -> AdminUser:
    admin_user = get_active_admin_user(session, current_user.sub)
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required.",
        )
    return admin_user


AdminUserDependency = Annotated[AdminUser, Depends(require_admin_user)]
