from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from .models import User, Task, Group
from . import db
from datetime import datetime

current_group_id = 0

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/create-group", methods=["GET", "POST"])
@login_required
def create_group():
    if request.method == "POST":
        group_name = request.form.get("text")
        if len(group_name) == 0:
            flash("Group name can't be empty.", category="error")
        group = Group(group_name)
        group.managers.append(current_user)
        group.members.append(current_user)
        current_user.groups.append(group)
        db.session.add(group)
        db.session.commit()
        flash("Group created.", category="success")
    
    return render_template("create_group.html", user=current_user)


@views.route("/tasks/<group_id>", methods=["GET", "POST"])
@login_required
def view_group(group_id):
    global current_group_id
    current_group_id = group_id
    group = Group.query.filter_by(id=group_id).first()
    if request.method == "POST":
        begin = request.form.get("begin")
        end = request.form.get("end")
        date_format = "%Y-%m-%d"
        begin = datetime.strptime(begin, date_format)
        end = datetime.strptime(end, date_format)
        text = request.form.get("text")
        if begin is None or end is None:
            flash("error", category="error")
        elif len(text) == 0:
            flash("Task can't be empty.", category="error")
        else:
            new_task = Task(text, begin, end)
            group.tasks.append(new_task)
            current_user.tasks.append(new_task)
            db.session.add(new_task)
            db.session.commit()
            flash("success", category="success")
    return render_template("group.html", user=current_user, group=group)