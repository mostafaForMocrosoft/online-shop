from extensions import db


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(15), nullable=False, default="pending")
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"))
    cart = db.relationship("Cart", back_populates="payments")


import models.cart
