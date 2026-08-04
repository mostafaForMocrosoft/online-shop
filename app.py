from os import makedirs
from flask import Flask
from blueprints.general import app as general
from blueprints.admin import app as admin
from blueprints.user import app as user
from config import database_url, SECRET_KEY, UPLOAD_DIR
from extensions import db, csrf, login_manager

app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app.register_blueprint(user)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_TRACk_MODIFICATIONS'] = False
app.config["SESSION_COOKIE_PATH"] = "/"
app.config["SESSION_COOKIE_NAME"] = "shop"

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict',
)
db.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)

makedirs(UPLOAD_DIR, exist_ok=True)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
