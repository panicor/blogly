"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    f_name = db.Column(db.Text, nullable = False)
    l_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text)

    @property
    def full_name(self):
        return f"{self.f_name} {self.l_name}"

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @property
    def date(self):
        return self.created_at.strftime("%Y, %H:%M")


def connect_db(app):
    db.app = app
    db.init_app(app)
