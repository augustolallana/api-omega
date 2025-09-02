from typing import Optional

from pydantic import BaseModel


class ImageBase(BaseModel):
    url: str
    alt_text: Optional[str] = None
    product_id: str


class ImageCreate(ImageBase):
    pass


class ImageUpdate(BaseModel):
    url: Optional[str] = None
    alt_text: Optional[str] = None
