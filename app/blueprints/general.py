from flask import Blueprint, render_template, flash, redirect, url_for
from app.models.product import Product

app = Blueprint("general", __name__)


@app.route("/")
def home():
    products = Product.query.filter(Product.active == True).all()
    return render_template("home.html", products=products)


@app.route("/detail-product/<int:id>")
def detail_product(id):
    p = Product.query.get(int(id))

    if not p:
        flash("محصول مورد نظر پیدا نشد", "warning")
        return redirect(url_for("general.home"))

    return render_template("detail-product.html", p=p)