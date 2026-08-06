from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User
from app.models.cart import Cart
from app.models.product import Product
from app.models.cart_item import CartItem

app = Blueprint("user", __name__)

@app.route("/user/login", methods = ['GET', "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter(User.username == username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("با موفقیت وارد حسابتان شدید", "warning")
                return redirect(url_for("user.dashboard"))
            else:
                flash("رمز عبور اشتباه است", "error")
                return redirect(url_for("user.login"))
        else:
            flash("نام کاربری وارد شده اشتباه است", "error")
            return redirect(url_for("user.login"))
    return render_template("user/login.html")


@app.route("/user/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        address = request.form.get("address")
        phone = int(request.form.get("phone"))
        password = request.form.get("password")

        is_user_exist = User.query.filter(User.username == username).filter(User.phone == phone).first()

        if is_user_exist:
            flash("نام کاربری یا شماره موبایل قبلا ثبت شده اند لطفا دوباره تلاش کنید", "warning")
            return redirect(url_for("user.register"))

        try:
            new_user = User(username=username, address=address, password=generate_password_hash(password), phone=phone)
            db.session.add(new_user)
            db.session.commit()
            flash("با موفقیت ثبت نام کرید", "success")
            return redirect(url_for("user.login"))
        except Exception as ex:
            print(ex)
            flash("نام کاربری وارد شده اشتباه است", "error")
            return redirect(url_for("user.register"))
    return render_template("user/register.html")


@app.route("/user/dashboard")
@login_required
def dashboard():
    return render_template("user/dashboard.html")


@app.route("/user/logout")
@login_required
def logout():
    logout_user()
    flash("شما با موفقیت از حسابتان خارج شدید", "info")
    return redirect(url_for("general.home"))


@app.route("/add-to-cart", methods = ['GET', "POST"])
@login_required
def add_to_cart():
    id = request.args.get("id")
    product = Product.query.get(int(id))

    if request.method == "POST":
        quantity_str = request.form.get("quantity")

        if not quantity_str or not quantity_str.isdigit():
            flash("تعداد وارد شده نامعتبر است", "error")
            return redirect(url_for("general.detail_product", id=id))

        quantity = int(quantity_str)
        if quantity <= 0:
            flash("تعداد باید بزرگتر از صفر باشد", "error")
            return redirect(url_for("general.detail_product", id=id))

        check_cart = current_user.carts.filter_by(status="pending").first()
        if check_cart:
            is_product_in_cart = check_cart.cart_items.filter(product_id=product.id).first()

            if is_product_in_cart:
                is_product_in_cart.quantity += int(quantity)
                flash("محصول به سبد خریدتان اضافه شد", "success")
                return redirect(url_for("user.carts"))
            new_cart_item = CartItem(quantity=1, product=product, cart=check_cart, price=product.price)
            db.session.add(new_cart_item)
            db.session.commit()
            flash("محصول به سبد خریدتان اضافه شد", "success")
            return redirect(url_for("user.carts"))
        new_cart = Cart(user=current_user)
        cart_item = CartItem(cart=new_cart, quantity=quantity, product=product, price=product.price)
        db.session.add(new_cart)
        db.session.add(cart_item)
        db.session.commit()
        flash("محصول به سبد خریدتان اضافه شد", "success")
        return redirect(url_for("user.carts"))
    return render_template("user/add-to-cart.html", p=product)


@app.route("/user/carts")
@login_required
def carts():
    cart = current_user.carts.filter_by(status="pending").first()
    return render_template("user/carts.html", cart=cart)