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
    image_url = db.Column(db.String(255), nullable=False, default="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Ffree-vector%2Fno-image-available&psig=AOvVaw3MW4bhjVsEqe4olMGfEe3z&ust=1693110580818000&source=images&cd=vfe&opi=89978449&ved=0CA8QjRxqFwoTCIDL08e--YADFQAAAAAdAAAAABAE")

