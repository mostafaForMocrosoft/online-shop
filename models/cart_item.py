from extensions import db


class CartItem(db.Model):
    __tablename__ = "cart_items"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"))
    product = db.relationship("Product", back_populates="cart_items")
    cart = db.relationship("Cart", back_populates="cart_items")
