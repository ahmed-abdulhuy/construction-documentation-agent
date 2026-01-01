from sqlmodel import select
from app.core.security import verify_password
from app.db.models.user import User
from app.db.models.schemas import UserCreate, UserUpdate
from typing import Any
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from app.db.main import getAsyncDB
from app.core.security import get_password_hash

async def get_user_by_email(*, session: AsyncSession, email: str) -> User | None:
    print('\n\nExecuting statement to get user by email:', email)
    statement = select(User).where(User.email == email)
    session_results = await session.exec(statement)
    session_user = session_results.first()
    return session_user


async def authenticate(*, session: AsyncSession, email: str, password: str) -> User | None:
    db_user = await get_user_by_email(session=session, email=email)
    print("\n\nDB User fetched for authentication:", db_user)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


async def create_user(*, session: AsyncSession, user_create: UserCreate) -> User:
    db_user = User(
        **user_create.model_dump(exclude={"password"}),
        hashed_password=get_password_hash(user_create.password),
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def update_user(*, session: AsyncSession, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

