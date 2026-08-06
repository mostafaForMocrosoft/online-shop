from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

import app.models.user
import app.models.product
import app.models.cart
import app.models.cart_item