from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app.config import admin_password, admin_username

app = Blueprint("admin", __name__, url_prefix="/admin")

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