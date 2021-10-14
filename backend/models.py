import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_script import Command
from backend.app import db, login


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_on = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())

    def __init__(self, username: str):
        self.username = username

    def __repr__(self):
        return f'<{self.id}:{self.username}>'

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)


# class Result(db.Model):
#     __tablename__ = 'tasks'
#
#     id = db.Column(db.Integer, primary_key=True)
#     uuid = db.Column(db.String(200), nullable=False)
#     msisdn = db.Column(db.Float, default=None)
#     radius = db.Column(db.Float, default=None)
#     delta = db.Column(db.Float, default=None)
#     status = db.Column(db.String(50), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
#
#     def __init__(self, uuid: str, status: str, user_id: int):
#         self.uuid = uuid
#         self.status = status
#         self.user_id = user_id
#
#     def __repr__(self):
#         return f'<id: {self.id}><{self.uuid}><{self.status}>, ' \
#                f'user_id: {self.user_id}, <{self.msisdn} - {self.radius} - {self.delta}>'
#
#     def set_status(self, status: str):
#         self.status = status
#
#     def set_attr(self, msisdn: float, radius: float, delta: float):
#         self.msisdn = msisdn
#         self.radius = radius
#         self.delta = delta


class UserTasks(db.Model):
    __tablename__ = 'user_tasks'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)

    def __init__(self, uuid: str, user_id: int):
        self.uuid = uuid
        self.user_id = user_id

    def __repr__(self):
        return f'<id: {self.id}><{self.uuid}><user_id: {self.user_id}>'


class InitDbCommand(Command):
    def run(self):
        print('Создание таблиц в базе данных...')
        init_db()
        print('Таблицы созданы!')


def init_db():
    db.drop_all()
    db.create_all()


@login.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)
