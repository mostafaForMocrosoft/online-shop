from flask import Blueprint, render_template, flash, redirect, url_for
from app.models.product import Product

app = Blueprint("general", __name__)


@app.route("/")
def home():
    products = Product.query.filter(Product.active == True).all()
    return render_template("home.html", products=products)