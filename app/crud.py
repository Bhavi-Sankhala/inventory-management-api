from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import (
    Product,
    ProductType,
    Brand,
    StockTransaction
)

# ---------- PRODUCT ----------
def create_product(db: Session, data):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_all_products(db: Session):
    return db.query(Product).all()


def update_product(db: Session, product_id: int, data):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    db.delete(product)
    db.commit()
    return True


# ---------- STOCK ----------
def stock_in(db: Session, product_id: int, quantity: int, remarks: str | None):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    product.quantity += quantity

    tx = StockTransaction(
        product_id=product_id,
        change_quantity=quantity,
        transaction_type="IN",
        remarks=remarks
    )

    db.add(tx)
    db.commit()
    db.refresh(product)
    return product


def stock_out(db: Session, product_id: int, quantity: int, remarks: str | None):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or product.quantity < quantity:
        return None

    product.quantity -= quantity

    tx = StockTransaction(
        product_id=product_id,
        change_quantity=-quantity,
        transaction_type="OUT",
        remarks=remarks
    )

    db.add(tx)
    db.commit()
    db.refresh(product)
    return product


def get_stock_history(db: Session, product_id: int):
    return (
        db.query(StockTransaction)
        .filter(StockTransaction.product_id == product_id)
        .order_by(StockTransaction.created_at.desc())
        .all()
    )


# ---------- PRODUCT TYPE ----------
def create_product_type(db: Session, name: str):
    try:
        pt = ProductType(name=name)
        db.add(pt)
        db.commit()
        db.refresh(pt)
        return pt
    except IntegrityError:
        db.rollback()
        return None


def get_all_product_types(db: Session):
    return db.query(ProductType).all()


# ---------- BRAND ----------
def create_brand(db: Session, name: str):
    try:
        brand = Brand(name=name)
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand
    except IntegrityError:
        db.rollback()
        return None


def get_all_brands(db: Session):
    return db.query(Brand).all()
