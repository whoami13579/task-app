from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from .models import User, Group
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in.", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password incorrect.", category="error")

        else:
            flash("User does not exist.", category="error")

    return render_template("login.html", user=current_user)


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
        elif len(password1) < 6:
            flash("Password should be at least 6 characters.", category="error")
        else:
            # user = User(email=email, username=username, password=generate_password_hash(password1, method="pbkdf2"))
            user = User(email, username, generate_password_hash(password1, method="pbkdf2"))
            group = Group(user.username+"\'s private group")
            user.groups.append(group)
            group.managers.append(user)
            group.members.append(user)
            db.session.add(user)
            db.session.add(group)
            db.session.commit()

            login_user(user, remember=True)
            flash("User created.", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@auth.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        user = User.query.filter_by(username=current_user.username).first()

        oldPassword = request.form.get("oldPassword")
        newPassword = request.form.get("newPassword")

        if user:
            if check_password_hash(current_user.password, oldPassword):
                if len(newPassword) < 6:
                    flash("New password should be at least 6 characters.", category="error")
                else:
                    current_user.password = generate_password_hash(newPassword, method="pbkdf2")
                    flash("Password changed", category="success")
                    db.session.commit()
            else:
                flash("Old password is wrong", category="error")
        else:
            flash("can't find user", category="error")
    return render_template("account.html", user=current_user)
