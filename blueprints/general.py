from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required, current_user
from extensions import db
from models.cart_item import CartItem
from models.product import Product
from models.cart import Cart

app = Blueprint("general", __name__)


@app.route("/")
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)


@app.route("/detail-product/<int:id>")
def detail_product(id):
    p = Product.query.get(int(id))

    if not p:
        flash("محصول پیدا نشد", "warning")
        return redirect(url_for("general.home"))

    return render_template("detail-product.html", p=p)


@app.route("/add-to-cart")
@login_required
def add_to_cart():
    id = request.args.get("id")
    quantity = request.args.get("quantity")

    product = Product.query.get(int(id))

    check_cart = current_user.carts.filter(Cart.status == "pending").first()

    if check_cart:
        if quantity <= product.stock:
            cart_item = CartItem(quantity=quantity, product=product, cart=check_cart)
            db.session.add(cart_item)
            db.session.commit()
            flash(f"محصول {product.name} به سبد خریدتان اضافه شد", "success")
            return redirect(url_for("user.dashboard"))
        flash("موجودی محصول کافی نیست", "error")
        return redirect(url_for("user.dashboard"))
    cart = Cart(user=current_user)
    db.session.add(cart)
    cart_item = CartItem(quantity=1, product=product, cart=cart)
    db.session.add(cart_item)
    db.session.commit()
    return "محصول به سبد خریدتان اضافه شد" + "<br>" + "<a href='/user/dashboard'>داشبورد</a>"
