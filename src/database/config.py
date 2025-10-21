from typing import Generator
from fastapi import Request, Depends, HTTPException, status
from sqlmodel import Session, SQLModel, create_engine, select

import firebase_admin
from firebase_admin import auth, credentials

from src.models.user import User
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
        
        
def create_firebase_auth() -> Generator[Session, None, None]:
    """Initialize Firebase Admin SDK."""
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_CRED)
        firebase_admin.initialize_app(cred)


async def get_current_user(
    request: Request,
):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="You are not authorized to access this resource.")

    try:
        id_token = auth_header.split(" ")[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]

        # Full Firebase user record
        firebase_user = auth.get_user(uid)

    except Exception:
        raise HTTPException(status_code=401, detail="You are not authorized to access this resource.")

    return {
        "firebase_user": firebase_user,
        "decoded_token": decoded_token,
    }