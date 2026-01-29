from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    product_type_id: int
    brand_id: int
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


class StockChange(BaseModel):
    quantity: int
    remarks: Optional[str] = None


class StockHistoryResponse(BaseModel):
    transaction_type: str
    change_quantity: int
    remarks: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class ProductTypeCreate(BaseModel):
    name: str


class BrandCreate(BaseModel):
    name: str
