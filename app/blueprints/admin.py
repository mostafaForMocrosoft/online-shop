from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from app.config import admin_password, admin_username
from app.models.product import Product
from app.extensions import db

app = Blueprint("admin", __name__, url_prefix="/admin")


@app.before_request
def before_request():
    if session.get("admin") != admin_username and request.endpoint != "admin.login":
        abort(403)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == admin_username and password == admin_password:
            session['admin'] = username
            return redirect(url_for("admin.dashboard"))
        else:
            flash("نام کاربری یا رمز ورود اشتباه است", "warning")
            return redirect(url_for("general.home"))
    return render_template("admin/login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")


@app.route("/dashboard/products", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        stock = int(request.form.get("stock"))
        price = int(request.form.get("price"))
        active = request.form.get("active")

        if active:
            active = True
        else:
            active = False

        try:
            product = Product(name=name, description=description, stock=stock, price=price, active=active)
            db.session.add(product)
            db.session.commit()
            flash("محصول با موفقیت اضافه شد")
            return redirect(url_for("admin.products"))
        except Exception as ex:
            print(ex)
            return "خطا " + "<br>" + "<a href='{{url_for(\"admin.dashboard\")}}'></a>"
    products = Product.query.all()
    return render_template("admin/products.html", products=products)


@app.route("/dashboard/edit-product/<int:id>", methods = ["GET", "POST"])
def edit_product(id):
    product = Product.query.get(int(id))

    if not product:
        flash("محصول مورد نظر پیدا نشد", "warning")
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        stock = int(request.form.get("stock"))
        price = int(request.form.get("price"))
        active = request.form.get("active")

        if active :
            active = True
        else:
            active = False

        try:
            product.name = name
            product.description = description
            product.stock = stock
            product.price = price
            product.active = active

            db.session.commit()
            flash("محصول مورد نظر ویرایش شد", "info")
            return redirect(url_for("admin.dashboard"))
        except Exception as ex:
            print(ex)
            flash("سیستم دچار مشکل شده", "warning")
            return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit-product.html", product=product)