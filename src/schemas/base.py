from typing import Any, Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status_code: int
    message: Optional[str] = None
    detail: Optional[Any] = None
