import os, psycopg
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.products import Product

from pydantic import BaseModel, ConfigDict
from typing import List, Optional

app = FastAPI()

class ProductCreate(BaseModel):
    sku: str
    name: str
    price: float

class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    price: float

    model_config = ConfigDict(from_attributes=True)

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли товар с таким же SKU
    existing_product = db.query(Product).filter(Product.sku == product_in.sku).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists"
        )
    
    db_product = Product(
        sku=product_in.sku,
        name=product_in.name,
        price=product_in.price
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product


@app.get("/products", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

def main() -> None:
    with psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "inventory"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]

    print(f"Connected to PostgreSQL: {version}")

if __name__ == "__main__":
    main()