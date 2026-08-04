from app.extensions import db
from sqlalchemy import *

class Product(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False)