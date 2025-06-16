from typing import Optional

from pydantic import BaseModel


class BrandBase(BaseModel):
    name: str
    description: str


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
