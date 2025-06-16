from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PromotionBase(BaseModel):
    name: str
    description: Optional[str] = None
    discount_percentage: float
    minimun_number_of_products: int
    start_date: datetime
    end_date: datetime


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    discount_percentage: Optional[float] = None
    minimun_number_of_products: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
