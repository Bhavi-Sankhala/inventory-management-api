from sqlalchemy.orm import Session
from .models import Product

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
