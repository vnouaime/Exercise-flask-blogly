"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """ Connect to a database """
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    image_url = db.Column(db.String(255), nullable=False, default="https://icon-library.com/images/no-picture-available-icon/no-picture-available-icon-20.jpg")

