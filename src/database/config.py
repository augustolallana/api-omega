from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from src.settings import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True to see SQL queries in console
)


def create_db_and_tables() -> None:
    """Create database tables for all SQLModel models."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency for database sessions."""
    with Session(engine) as session:
        yield session
