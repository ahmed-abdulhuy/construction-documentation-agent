from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from app.db.main import getAsyncDB
from sqlmodel.ext.asyncio.session import AsyncSession
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from app.db.models import TokenPayload, User
from app.core.env_settings import ENV_VARS
from app.db.models import User
from fastapi.security import OAuth2PasswordBearer


# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{ENV_VARS.API_V1_STR}/login/access-token"
# )
async def get_current_user(
        request: Request,
        session: Annotated[AsyncSession , Depends(getAsyncDB)], 
        # token: Annotated[str, Depends(reusable_oauth2)]
        ) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )
    try:
        payload = jwt.decode(
            token, ENV_VARS.SECRET_KEY, algorithms=[ENV_VARS.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def get_current_active_superuser(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
