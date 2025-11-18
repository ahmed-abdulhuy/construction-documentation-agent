from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.models import *
from app.core.env_settings import ENV_VARS
from sqlmodel import select
from app.core.security import get_password_hash

# Create an asynchronous database engine
print("Creating engine with DATABASE_URL:", ENV_VARS.DATABASE_URL)
engine = create_async_engine(url=ENV_VARS.DATABASE_URL, echo=True)
print("Engine created successfully.", engine)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_first_superuser():
    async with SessionLocal() as session:
        # Check if a superuser already exists
        result = await session.exec(select(User).where(User.is_superuser == True))
        existing_superuser = result.first()

        if existing_superuser:
            print("Superuser already exists:", existing_superuser.email)
            return

        # Create a new superuser
        user = User(
            email="admin@example.com",
            name="Admin User",
            is_superuser=True,
            is_active=True,
            hashed_password=get_password_hash("FFI_CONTRACTING2024!"),
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        print("Superuser created successfully:", user.email)


# Initialize database tables based on SQLModel definitions
async def initDB():
    async with engine.begin() as conn:
        # Run the synchronous SQLModel.metadata.create_all in async mode
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Database tables created successfully.")

    await create_first_superuser()
 

async def getAsyncDB():
    """Dependency to get async database session"""
    async with SessionLocal() as session:
        yield session
