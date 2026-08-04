from flask import Blueprint

app = Blueprint("admin", __name__, url_prefix="/admin")

@app.route("/login")
def login():
    return "LOGIN ADMIN"