from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func


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
    tasks = db.relationship('Task', backref='user', passive_deletes=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.DateTime(timezone=True))
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete="CASCADE"), nullable=False)
