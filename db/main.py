from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import Config

# Create an asynchronous database engine
print("Creating engine with DATABASE_URL:", Config.DATABASE_URL)
engine = create_async_engine(url=Config.DATABASE_URL, echo=True)
print("Engine created successfully.", engine)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Initialize database tables based on SQLModel definitions
async def initDB():
    async with engine.begin() as conn:
        # Run the synchronous SQLModel.metadata.create_all in async mode
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Database tables created successfully.")
 

async def getAsyncDB():
    """Dependency to get async database session"""
    async with SessionLocal() as session:
        yield session
