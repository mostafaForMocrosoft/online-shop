from app.extensions import db
from sqlalchemy import *

class Cart(db.Model):
    __tablename__ = "carts"
    id = Column(Integer, primary_key=True)
    status = Column(String, default="pending", nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="carts")

    cart_items = db.relationship("CartItem", back_populates="cart")