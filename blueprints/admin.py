from flask import Blueprint, render_template, request, session, redirect, flash, abort
from config import ADMIN_USERNAME, ADMIN_PASSWORD
from models.cart import Cart
from models.product import Product
from extensions import db
from os import path
from config import UPLOAD_DIR

app = Blueprint("admin", __name__, url_prefix="/admin")


@app.before_request
def before_request():
    if session.get("admin") != "admin" and request.endpoint != "admin.login":
        abort(403)


@app.route("/login", methods=['GET', "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = "admin"
            return redirect("/admin/dashboard")
        else:
            return redirect("/admin/login")
    return render_template("admin/login.html")


@app.route("/dashboard")
def dashboard():
    carts = Cart.query.all()
    return render_template("admin/dashboard.html", carts=carts)


@app.route("/dashboard/products", methods=['GET', "POST"])
def add_product():
    if request.method == "POST":
        file = request.files.get("file")
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        stock = request.form.get("stock")
        active = request.form.get("active")

        price = int(price)
        stock = int(stock)

        try:
            if active == None:
                product = Product(name=name, description=description, price=price, stock=stock, active=0)
            else:
                product = Product(name=name, description=description, price=price, stock=stock, active=1)

            db.session.add(product)
            db.session.commit()
            file.save(path.join(UPLOAD_DIR, f"{product.id}.jpg"))
            return "محصول اضافه شد" + " <br> <a href='/admin/dashboard/products'>محصولات</a>"
        except Exception:
            return "خطا" + "<br>" + "<a href='/admin/dashboard'>dashboard</a>"
    products = Product.query.all()
    return render_template("admin/products.html", products=products)


@app.route("/admin/dashboard/edit_product/<int:id>", methods=['GET', "POST"])
def edit_product(id):
    pk = int(id)
    product = Product.query.get(pk)
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        stock = request.form.get("stock")
        price = request.form.get("price")
        active = request.form.get("active")

        try:
            product.name = name
            product.description = description
            product.stock = int(stock)
            product.price = int(price)
            if active:
                active = 1
            else:
                active = 0
            product.active = active

            db.session.commit()

            return "محصول با موفقیت ارایش شد" + "<br>" + "<a href='/admin/dashboard/products'>محصولات</a>"
        except BaseException:
            flash("سرور با خطایی مواجه شد", "error")
            return redirect("/admin/dashboard/products")
    else:
        if not product:
            flash("محصول پیدا نشد", "warning")
            return redirect("/admin/dashboard/products")
        return render_template("admin/edit_product.html", product=product)


@app.route("/admin/admin/dashboard/remove-product/<int:id>")
def remove_product(id):
    p = Product.query.get(int(id))

    if not p:
        flash("محصول مورد نظر پیدا نشد", "warning")
        return redirect("/admin/dashboard/products")

    try:
        db.session.delete(p)
        db.session.commit()
        return "محصول با موفقیت حذف شد" + "<br> <a href='/admin/dashboard/products'>محصولات</a>"
    except Exception:
        return "خطا" + "<br> <a href='/admin/dashboard'>dashboard</a>"
