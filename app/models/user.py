from flask_login import UserMixin
from app.extensions import db
from sqlalchemy import *

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, nullable=False)
    address = Column(Text, unique=False, nullable=False)
    phone = Column(Integer, unique=True, nullable=False)
    password = Column(String(170), unique=False, nullable=False)

    carts = db.relationship("Cart", back_populates="user")