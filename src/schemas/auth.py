from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Token model for authentication."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model for authentication."""

    email: Optional[str] = None
