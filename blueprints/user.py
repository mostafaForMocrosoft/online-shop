from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from flask_login import login_user, current_user, login_required, logout_user

app = Blueprint("user", __name__, url_prefix="/user")


@app.route("/register", methods=['GET', "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        phone = request.form.get("phone")
        address = request.form.get("address")
        password = request.form.get("password")

        is_user_exist = User.query.filter(User.username == username).filter(User.phone == phone).first()

        if is_user_exist:
            flash("نام کاربری یا شماره موبایل تکراری است", "warning")
            return redirect(url_for("user.register"))

        try:
            user = User(username=username, phone=phone, address=address)
            user.password = generate_password_hash(password)
            db.session.add(user)
            db.session.commit()
            flash("با موفقیت یک حساب ساختید", "success")
            return redirect(url_for("user.login"))
        except Exception:
            return "سرور با خطایی مواجه شد" + "<br> <a href='/user/register'>ثبت نام</a>"
    return render_template("user/register.html")


@app.route("/login", methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if current_user.is_authenticated:
            flash("شما وارد حسابتان شده اید", "info")
            return redirect(url_for("user.dashboard"))

        try:
            user = User.query.filter(User.username == username).first()
            if user:
                if check_password_hash(user.password, password):
                    flash("شما با موفقیت وارد حسابتان شدید", "success")
                    login_user(user)
                    return redirect(url_for("user.dashboard"))
                else:
                    flash("رمز عبور اشتباه است", "warning")
                    return redirect(url_for("user.login"))
            else:
                flash("نام کاربری وارد شده اشتباه است", "warning")
                return redirect(url_for("user.login"))
        except Exception as ex:
            print(ex)
            return "سرور با خطایی مواجه شد" + "<br>" + "<a href='/user/login'>ورود</a>"
    return render_template("user/login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("user/dashboard.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("شما با موفقیت خارج شدید بعدا سر بزنی ها!", "info")
    return redirect(url_for("general.home"))
