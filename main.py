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