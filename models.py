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

    posts = db.relationship('Post', backref='user', cascade='all')

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

class PostTag(db.Model):

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship("Post", secondary='posts_tags', backref='tags')

def connect_db(app):
    db.app = app
    db.init_app(app)
