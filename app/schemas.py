from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
    description: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    is_active: bool

    class Config:
        from_attributes = True
