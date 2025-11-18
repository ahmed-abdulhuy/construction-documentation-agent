import uuid
from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import col, delete, func, select
from fastapi.security import OAuth2PasswordBearer
from app.db.main import getAsyncDB
from sqlmodel.ext.asyncio.session import AsyncSession
from app.utils import db_utils
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from app.db.models import TokenPayload, User

from app.core.env_settings import ENV_VARS
from app.core.security import get_password_hash, verify_password
from app.db.models import (
    Message,
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from app.utils.utils import generate_new_account_email, send_email


router = APIRouter(prefix="/users", tags=["users"])
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{ENV_VARS.API_V1_STR}/login/access-token"
)


async def get_current_user(session: Annotated[AsyncSession , Depends(getAsyncDB)], token: Annotated[str, Depends(reusable_oauth2)]) -> User:
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


# GET All Users
@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
async def read_users(session: Annotated[AsyncSession, Depends(getAsyncDB)], skip: int = 0, limit: int = 100):
    """
    Retrieve users.
    """
    print("\n\nRead Users", skip, limit)
    count_statement = select(func.count()).select_from(User)
    result = await session.exec(count_statement)
    count = result.one()

    statement = select(User).offset(skip).limit(limit)
    result = await session.exec(statement)
    users = result.all()


    return UsersPublic(data=users, count=count)


# Create User 
@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
async def create_user(*, session: Annotated[AsyncSession, Depends(getAsyncDB)], user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = await db_utils.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = await db_utils.create_user(session=session, user_create=user_in)
    # if ENV_VARS.emails_enabled and user_in.email:
    #     email_data = generate_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    #     send_email(
    #         email_to=user_in.email,
    #         subject=email_data.subject,
    #         html_content=email_data.html_content,
    #     )
    return user


@router.patch("/me", response_model=UserPublic)
async def update_user_me(
    *, session: Annotated[AsyncSession, Depends(getAsyncDB)], user_in: UserUpdateMe, current_user: Annotated[User, Depends(get_current_user)]
) -> Any:
    """
    Update own user.
    """

    if user_in.email:
        existing_user = await db_utils.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    print("\n\nUpdated current user data:", current_user)
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)
    return current_user


@router.patch("/me/password", response_model=Message)
async def update_password_me(
    *, session: Annotated[AsyncSession, Depends(getAsyncDB)], body: UpdatePassword, current_user: Annotated[User, Depends(get_current_user)]
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    await session.commit()
    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: Annotated[User, Depends(get_current_user)]) -> Any:
    """
    Get current user.
    """
    return current_user


@router.delete("/me", response_model=Message)
async def delete_user_me(session: Annotated[AsyncSession, Depends(getAsyncDB)], current_user: Annotated[User, Depends(get_current_user)]) -> Any:
    """
    Delete own user.
    """
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    session.delete(current_user)
    await session.commit()
    return Message(message="User deleted successfully")


@router.post("/signup", response_model=UserPublic)
async def register_user(session: Annotated[AsyncSession, Depends(getAsyncDB)], user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = await db_utils.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = await db_utils.create_user(session=session, user_create=user_create)
    return user


@router.get("/{user_id}", response_model=UserPublic)
async def read_user_by_id(
    user_id: uuid.UUID, session: Annotated[AsyncSession, Depends(getAsyncDB)], current_user: Annotated[User, Depends(get_current_user)]
) -> Any:
    """
    Get a specific user by id.
    """
    user = await session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
async def update_user(
    *,
    session: Annotated[AsyncSession, Depends(getAsyncDB)],
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """

    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = await db_utils.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = await db_utils.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
async def delete_user(
    session: Annotated[AsyncSession, Depends(getAsyncDB)], current_user: Annotated[User, Depends(get_current_user)], user_id: uuid.UUID
) -> Message:
    """
    Delete a user.
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    await session.delete(user)
    await session.commit()
    return Message(message="User deleted successfully")