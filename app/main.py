from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal
from . import schemas, crud

app = FastAPI(title="Inventory Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    return crud.create_product(db, product)

@app.post("/products", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    return crud.create_product(db, product)

@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    data: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    product = crud.update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

