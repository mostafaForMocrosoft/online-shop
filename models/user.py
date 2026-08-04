from extensions import db
from flask_login import UserMixin
from extensions import login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    carts = db.relationship("Cart", back_populates="user", lazy="dynamic")


from models.cart import Cart


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
