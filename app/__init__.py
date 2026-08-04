def create_app():
    from flask import Flask
    from app.extensions import db
    from app.config import database_url
    from app.blueprints.general import app as general
    from app.blueprints.admin import app as admin
    from app.blueprints.user import app as user
    from app.config import SECRET_KEY

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.secret_key = SECRET_KEY
    app.register_blueprint(general)
    app.register_blueprint(user)
    app.register_blueprint(admin)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app