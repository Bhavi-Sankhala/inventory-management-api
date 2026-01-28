from sqlalchemy import Column, Integer, String, Boolean, Numeric, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP)

class StockTransaction(Base):
    __tablename__ = "stock_transactions"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    change_quantity = Column(Integer)
    transaction_type = Column(String(10))
    remarks = Column(Text)
    created_at = Column(TIMESTAMP)
