from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User

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