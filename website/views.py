from flask import Blueprint, render_template
from flask_login import current_user, login_required

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)







@views.route("/task")
@login_required
def task():
    return render_template("task.html", user=current_user)
