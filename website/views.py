from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User, Task, Group
from . import db
from datetime import datetime

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


@views.route("/group/<group_id>", methods=["GET", "POST"])
@login_required
def view_group(group_id):
    group = Group.query.filter_by(id=group_id).first()
    if request.method == "POST":
        begin = request.form.get("begin")
        end = request.form.get("end")
        date_format = "%Y-%m-%d"
        begin = datetime.strptime(begin, date_format)
        end = datetime.strptime(end, date_format)

        beginString = str(begin)
        endString = str(end)
        year1 = int(beginString[0:4])
        year2 = int(endString[0:4])
        month1 = int(beginString[5:7])
        month2 = int(endString[5:7])
        day1 = int(beginString[8:10])
        day2 = int(endString[8:10])

        text = request.form.get("text")
        if begin is None or end is None:
            flash("error", category="error")
        elif len(text) == 0:
            flash("Task can't be empty.", category="error")
        elif year2 < year1:
            flash("The task ends before it begins", category="error")
        elif (year1 <= year2) and (month2 < month1):
            flash("The task ends before it begins", category="error")
        elif (year1 <= year2) and (month1 <= month2) and (day2 < day1):
            flash("The task ends before it begins", category="error")
        else:
            new_task = Task(text, begin, end)
            group.tasks.append(new_task)
            current_user.tasks.append(new_task)
            db.session.add(new_task)
            db.session.commit()
            flash("success", category="success")
    return render_template("group.html", user=current_user, group=group)


@views.route("/delete/<task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return redirect(url_for("views.home"))

    group = Group.query.filter_by(id=task.group[0].id).first()
    author = User.query.filter_by(id=task.author[0].id).first()
    managers = []
    for user in group.managers:
        managers.append(user.id)

    if current_user.id in managers or current_user.id == task.author:
        author.tasks.remove(task)
        group.tasks.remove(task)
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted.", category="success")
    else:
        flash("Error", category="error")
        return redirect(url_for("views.home"))

    return redirect(url_for("views.view_group", group_id=group.id))


@views.route("/join-group", methods=["GET", "POST"])
@login_required
def join_group():
    if request.method == "POST":
        group_name = request.form.get("text")
        if len(group_name) == 0:
            flash("Group name can't be empty.", category="error")
        group = Group.query.filter_by(group_name=group_name).first()
        if group:
            members = []
            for user in group.members:
                members.append(user.id)
            if current_user.id in members:
                pass
            else:
                current_user.groups.append(group)
                group.members.append(current_user)
                db.session.commit()
            flash("Joined", category="success")
        else:
            flash("Group doesn't exist.", category="error")

    # return redirect(url_for("views.view_group"))
    return render_template("join.html", user=current_user)


@views.route("/leave-group/<group_id>")
@login_required
def leave_group(group_id):
    group = Group.query.filter_by(id=group_id).first()
    user = User.query.filter_by(id=current_user.id).first()
    if group and user:
        managers = []
        members = []
        for tmp_user in group.managers:
            managers.append(tmp_user.id)

        for tmp_user in group.members:
            members.append(tmp_user.id)

        if user.id in managers:
            group.managers.remove(user)

        if user.id in members:
            group.members.remove(user)
            user.groups.remove(group)

        db.session.commit()
    else:
        flash("error", category="error")
    return redirect(url_for("views.home", user=current_user))
