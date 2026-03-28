from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

class AutoPart(Base):
    __tablename__ = "auto_parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)           # Название (например, "Тормозные колодки")
    part_number = Column(String, unique=True, index=True, nullable=False) # Артикул
    price = Column(Float, nullable=False)           # Цена
    description = Column(String, nullable=True)     # Описание

    # Автоматические метки
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Soft Delete
    deleted_at = Column(DateTime, nullable=True)