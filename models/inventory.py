from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    
    quantity_on_hand = Column(Integer, default=0, nullable=False)      # Физический остаток
    quantity_reserved = Column(Integer, default=0, nullable=False)     # Зарезервировано

    # Связи для удобных запросов в SQLAlchemy
    warehouse = relationship("Warehouse", back_populates="inventory_items")
    product = relationship("Product")

    # Главное ограничение: на одном складе не может быть двух одинаковых записей для одного товара
    __table_args__ = (
        UniqueConstraint('product_id', 'warehouse_id', name='uq_product_warehouse'),
    )