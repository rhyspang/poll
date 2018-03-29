# -*- coding: utf-8 -*-

from poll import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))

    time_created = db.Column(db.DateTime(timezone=True),
                             server_default=db.func.now())
    time_updated = db.Column(db.DateTime(timezone=True),
                             onupdate=db.func.now())
    level = db.Column(db.Integer, default=2)

    files = db.relationship('LabellingFile', backref='user', lazy='dynamic')

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class LabellingFile(db.Model):
    __tablename__ = 'labelling_files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_uri = db.Column(db.String(512), unique=True)
    label = db.Column(db.String(512))
    prediction = db.Column(db.String(512))

    time_created = db.Column(db.DateTime(timezone=True),
                             server_default=db.func.now())
    time_updated = db.Column(db.DateTime(timezone=True),
                             onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=True)


