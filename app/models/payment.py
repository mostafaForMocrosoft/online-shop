from app.extensions import db
from datetime import datetime

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    amount = db.Column(db.Integer, nullable=False) # به ریال
    token = db.Column(db.String, nullable=False)

    status = db.Column(db.String(20), default="pending", nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="payments")

    @property
    def price_at_toman(self):
        return self.amount // 10