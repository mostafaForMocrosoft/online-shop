from flask import Blueprint

app = Blueprint("user", __name__, url_prefix="/user")

@app.route("/login")
def login():
    return "LOGIN USER"