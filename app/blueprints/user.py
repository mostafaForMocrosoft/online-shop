from flask import Blueprint

app = Blueprint("user", __name__)

@app.route("/user/login")
def login():
    return "LOGIN USER"