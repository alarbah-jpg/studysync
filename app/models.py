import secrets
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager

TASK_STATUSES = ("To Do", "In Progress", "Done")


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    memberships = db.relationship("Membership", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    join_code = db.Column(db.String(12), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    memberships = db.relationship("Membership", back_populates="group", cascade="all, delete-orphan")
    study_sessions = db.relationship("StudySession", back_populates="group", cascade="all, delete-orphan")
    tasks = db.relationship("Task", back_populates="group", cascade="all, delete-orphan")

    @staticmethod
    def new_join_code():
        while True:
            code = secrets.token_hex(3).upper()
            if not Group.query.filter_by(join_code=code).first():
                return code


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="member")  # "admin" or "member"
    __table_args__ = (db.UniqueConstraint("user_id", "group_id", name="uq_user_group"),)
    user = db.relationship("User", back_populates="memberships")
    group = db.relationship("Group", back_populates="memberships")

    @property
    def is_admin(self):
        return self.role == "admin"


class StudySession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    topic = db.Column(db.String(200), default="")
    start_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), default="")
    group = db.relationship("Group", back_populates="study_sessions")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="To Do")
    assignee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    group = db.relationship("Group", back_populates="tasks")
    assignee = db.relationship("User")
