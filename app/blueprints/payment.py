from flask import Blueprint, flash, redirect, url_for
from app.models.payment import Payment
from app.extensions import db
from flask_login import current_user, login_required
import requests

app = Blueprint("payment", __name__)


@app.route("/payment/<int:id>")
@login_required
def payment(id):
    cart = current_user.carts.filter_by(id=id, status="pending").first()
    try:
        r = requests.post("https://sandbox.shepa.com/api/v1/token", data={"api":"sandbox", "callback":"http://localhost:5000/verify", "amount":cart.total_price() * 10})
    except ConnectionError:
        flash("اینترنت شما قطع شد", "error")
        return redirect(url_for("user.carts"))
    else:
        if r.status_code != 200:
            print("اتصال به درگاه پرداخت نا موفق بود با status code {}".format(r.status_code))
            flash("خطا در اتصال به درگاه پرداخت", "error")
            return redirect(url_for("user.carts"))

        data = r.json()

        token = data['result']['token']
        url = data['result']["url"]

        new_payment = Payment(user=current_user, amount=cart.total_price() * 10, token=token)
        db.session.add(new_payment)
        db.session.commit()

        return redirect(url)