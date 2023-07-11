from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from .models import User, Task
from . import db
from datetime import datetime

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/create-task", methods=["GET", "POST"])
@login_required
def task():
    if request.method == "POST":
        begin = request.form.get("begin")
        end = request.form.get("end")
        date_format = "%Y-%m-%d"
        begin = datetime.strptime(begin, date_format)
        end = datetime.strptime(end, date_format)
        text = request.form.get("text")
        if begin is None or end is None:
            flash("error", category="error")
        else:
            # print(type(begin))
            # print(type(end))
            new_task = Task(text, begin, end, current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash("success", category="success")

    return render_template("create_task.html", user=current_user)


@views.route("/view-tasks")
@login_required
def view_tasks():
    tasks = Task.query.filter_by(author=current_user.id).all()
    return render_template("view_tasks.html", user=current_user, tasks=tasks)