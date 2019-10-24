from datetime import datetime, timedelta

from Prefix1_App import db


class User(db.Model):
    name = db.Column(db.Text, primary_key=True)
    access_key = db.Column(db.Text)
    tokens = db.relationship('Token', backref='user', lazy='dynamic')

    def to_dict(self):
        return {"name": self.name, "access_key": self.access_key}


class Token(db.Model):
    username = db.Column(db.Text, db.ForeignKey('user.name'))
    token = db.Column(db.Text, primary_key=True)
    valid = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(days=7))

    def to_dict(self):
        return {"username": self.username, "token": self.token, "valid":self.valid}
