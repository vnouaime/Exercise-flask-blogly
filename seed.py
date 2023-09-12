""" Seed file to make sample data for dbs """

from models import User, Post, db, connect_db, default_image
from app import app
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

db.drop_all()
db.create_all()

Post.query.delete()
User.query.delete()

new_user_1 = User(first_name="Vera", last_name="Nouaime")
new_user_2 = User(first_name="John", last_name="Smith")
new_user_3 = User(first_name="Susie", last_name="Sal")

db.session.add_all([new_user_1, new_user_2, new_user_3])
db.session.commit()

# Posts for Vera
user_1_post_1 = Post(title="First Post", content="This is my first post!", created_at=datetime.now(), user_FK=new_user_1.id)
user_1_post_2 = Post(title="Second Post", content="This is my second post!", created_at=datetime.now(), user_FK=new_user_1.id)
user_1_post_3 = Post(title="Third Post", content="This is my third post!", created_at=datetime.now(), user_FK=new_user_1.id)

# Posts for John
user_2_post_1 = Post(title="First Post", content="This is my first post!", created_at=datetime.now(), user_FK=new_user_2.id)
user_2_post_2 = Post(title="Second Post", content="This is my second post!", created_at=datetime.now(), user_FK=new_user_2.id)
user_2_post_3 = Post(title="Third Post", content="This is my third post!", created_at=datetime.now(), user_FK=new_user_2.id)

# Posts for Susie
user_3_post_1 = Post(title="First Post", content="This is my first post!", created_at=datetime.now(), user_FK=new_user_3.id)
user_3_post_2 = Post(title="Second Post", content="This is my second post!", created_at=datetime.now(), user_FK=new_user_3.id)
user_3_post_3 = Post(title="Third Post", content="This is my third post!", created_at=datetime.now(), user_FK=new_user_3.id)

db.session.add_all([
    user_1_post_1,
    user_1_post_2,
    user_1_post_3,
    user_2_post_1,
    user_2_post_2,
    user_2_post_3,
    user_3_post_1,
    user_3_post_2,
    user_3_post_3
]) 
db.session.commit()