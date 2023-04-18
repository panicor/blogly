"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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

def connect_db(app):
    db.app = app
    db.init_app(app)
