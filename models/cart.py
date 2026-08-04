from extensions import db


class Cart(db.Model):
    __tablename__ = "carts"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(15), default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="carts")

    payments = db.relationship("Payment", back_populates="cart")
    cart_items = db.relationship("CartItem", back_populates="cart")


from models.user import User
from models.payment import Payment
