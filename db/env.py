import src.db.models  # Import your models
from sqlmodel import SQLModel
from src.config import Config

# Database URL
database_url = Config.DATABASE_URL

# Set the database URL in Alembic's config
config = context.config
config.set_main_option("sqlalchemy.url", database_url)

# Metadata for migrations
target_metadata = SQLModel.metadata
