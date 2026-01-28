from sqlalchemy.orm import Session
from .models import Product
from .models import Product, StockTransaction


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
