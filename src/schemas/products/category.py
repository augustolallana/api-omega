from typing import Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str
    parent_id: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[str] = None
