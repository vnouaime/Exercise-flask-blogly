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
    
    posts = db.relationship('Post', backref='user')

    @property
    def get_full_name(self): 
        """ Returns full name of the user """

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """ New post with attributes of id, title, content, create_at timestamp, and user_FK. 
    user_FK is a foreign key connected to user model id """

    __tablename__="posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=False)
    content = db.Column(db.String(1000), nullable=False, unique=False)
    created_at = db.Column(db.DateTime, nullable=False)
    user_FK = db.Column(db.ForeignKey('users.id'), nullable=False)
    
    tags = db.relationship('Tag', secondary="posts_tags", backref="posts")
    
class Tag(db.Model): 
    """ New tag with attributes of id and name. """
    __tablename__="tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
class PostTag(db.Model): 
    """ Middle table for M2M relationship between Post and Tag """
    __tablename__="posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)