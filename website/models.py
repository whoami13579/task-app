from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func

user_group = db.Table("user_group",
                      db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                      db.Column("group_id", db.Integer, db.ForeignKey("group.id"))
                      )

user_task = db.Table("user_task",
                     db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                     db.Column("task_id", db.Integer, db.ForeignKey("task.id"))
                     )

group_task = db.Table("group_task",
                      db.Column("group_id", db.Integer, db.ForeignKey("group.id")),
                      db.Column("task_id", db.Integer, db.ForeignKey("task.id"))
                      )

group_manager = db.Table("group_manager",
                      db.Column("group_id", db.Integer, db.ForeignKey("group.id")),
                      db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
                      )
group_member = db.Table("group_member",
                      db.Column("group_id", db.Integer, db.ForeignKey("group.id")),
                      db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
                      )

class User(db.Model, UserMixin):
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # tasks = db.relationship('Task', backref="user", passive_deletes=True)
    # groups = db.relationship('Group', backref="user", passive_deletes=True)
    groups = db.relationship('Group', secondary=user_group, backref="member")
    tasks = db.relationship('Task', secondary=user_task, backref="author")


class Task(db.Model):
    def __init__(self, text, begin, end):
        self.text = text
        self.begin = begin
        self.end = end

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    begin = db.Column(db.DateTime(timezone=True))
    end = db.Column(db.DateTime(timezone=True))
    # author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    # group = db.Column(db.Integer, db.ForeignKey("group.id", ondelete="CASCADE"), nullable=False)


class Group(db.Model):
    def __init__(self, group_name):
        self.group_name = group_name

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(150), unique=True)
    managers = db.relationship("User", secondary=group_manager, backref="managerto")
    members = db.relationship("User", secondary=group_member, backref="memberto")
    tasks = db.relationship("Task", secondary=group_task, backref="group")
    # manager = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    # tasks = db.relationship("Task", backref="group", passive_deletes=True)

# class AllGroups(db.Model):
#     def __init__(self, group_id, group_name,member_id):
#         self.group_id = group_id
#         self.group_name = group_name
#         self.group_id = member_id

#     id = db.Column(db.Integer, primary_key=True)
#     group_id = db.Column(db.Integer)
#     group_name = db.Column(db.String(150))
#     member_id = db.Column(db.Integer)
