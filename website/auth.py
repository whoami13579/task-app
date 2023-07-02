from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user

auth = Blueprint("auth", __name__)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    return render_template("signup.html", user=current_user)
