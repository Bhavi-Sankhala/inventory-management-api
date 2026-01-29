from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal
from . import schemas, crud
from .models import ProductType, Brand

app = FastAPI(title="Inventory Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- PRODUCTS ----------
@app.post("/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    if not db.query(ProductType).filter(ProductType.id == product.product_type_id).first():
        raise HTTPException(status_code=400, detail="Invalid product type")

    if not db.query(Brand).filter(Brand.id == product.brand_id).first():
        raise HTTPException(status_code=400, detail="Invalid brand")

    return crud.create_product(db, product)


@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)


@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = crud.update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


# ---------- STOCK ----------
@app.post("/products/{product_id}/stock-in", response_model=schemas.ProductResponse)
def stock_in_api(product_id: int, data: schemas.StockChange, db: Session = Depends(get_db)):
    product = crud.stock_in(db, product_id, data.quantity, data.remarks)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products/{product_id}/stock-out", response_model=schemas.ProductResponse)
def stock_out_api(product_id: int, data: schemas.StockChange, db: Session = Depends(get_db)):
    product = crud.stock_out(db, product_id, data.quantity, data.remarks)
    if not product:
        raise HTTPException(status_code=400, detail="Insufficient stock or product not found")
    return product


@app.get("/products/{product_id}/stock-history", response_model=list[schemas.StockHistoryResponse])
def stock_history_api(product_id: int, db: Session = Depends(get_db)):
    return crud.get_stock_history(db, product_id)


# ---------- PRODUCT TYPES ----------
@app.post("/product-types")
def create_product_type(data: schemas.ProductTypeCreate, db: Session = Depends(get_db)):
    pt = crud.create_product_type(db, data.name)
    if not pt:
        raise HTTPException(status_code=400, detail="Product type already exists")
    return pt


@app.get("/product-types")
def get_product_types(db: Session = Depends(get_db)):
    return crud.get_all_product_types(db)


# ---------- BRANDS ----------
@app.post("/brands")
def create_brand(data: schemas.BrandCreate, db: Session = Depends(get_db)):
    brand = crud.create_brand(db, data.name)
    if not brand:
        raise HTTPException(status_code=400, detail="Brand already exists")
    return brand


@app.get("/brands")
def get_brands(db: Session = Depends(get_db)):
    return crud.get_all_brands(db)
