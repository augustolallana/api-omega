from typing import Any, Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """Base response model for all API responses."""

    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None
