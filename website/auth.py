from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from .models import User
from werkzeug.security import generate_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if User.query.filter_by(email=email).first():
            flash("Email is already in use.", category="error")
        elif User.query.filter_by(username=username).first():
            flash("Username is already in use.", category="error")
        elif password1 != password2:
            flash("Password don\'t match.", category="error")
        elif len(email) < 1:
            flash("Email can not be empty.", category="error")
        elif len(username) < 1:
            flash("Username can not be empty.", category="error")
        else:
            # user = User(email=email, username=username, password=generate_password_hash(password1, method="pbkdf2"))
            user = User(email=email, username=username, password=password1)
    return render_template("signup.html", user=current_user)
