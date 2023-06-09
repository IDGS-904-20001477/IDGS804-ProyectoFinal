from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TINYINT
from .db import db


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    status = db.Column(TINYINT, default=1)
    created_at = db.Column(db.DateTime())


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(255))
    status = db.Column(TINYINT, default=1)
    created_at = db.Column(db.DateTime())


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Integer(), nullable=False, default=2)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))


class User_Profile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer(), primary_key=True)
    lastname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    status = db.Column(TINYINT, default=1)
    created_at = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
