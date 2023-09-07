"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_image = "https://icon-library.com/images/no-picture-available-icon/no-picture-available-icon-20.jpg"

def connect_db(app):
    """ Connect to a database """
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ New user with attributes of id, first name, last name, and image url. If user does
    not provide image, default one will be given """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=True)
    image_url = db.Column(db.String(255), nullable=False, default=default_image)

    @property
    def get_full_name(self): 
        """ Returns full name of the user """

        return f"{self.first_name} {self.last_name}"

