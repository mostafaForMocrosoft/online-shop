from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.login_message = "اول وارد حسابتان شوید و بعد هر صفحه ای را خواستید باز کنید"
login_manager.login_message_category = "warning"

import app.models.user
import app.models.product
import app.models.cart
import app.models.cart_item
import app.models.payment