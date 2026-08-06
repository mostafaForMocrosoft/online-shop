from app.extensions import db
from sqlalchemy import *

class CartItem(db.Model):
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product = db.relationship("Product")
    cart = db.relationship("Cart", back_populates="cart_items")