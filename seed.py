""" Seed file to make sample data for dbs """
import os
from models import User, Post, Tag, PostTag, db, connect_db, default_image
from app import app
from datetime import datetime

if os.environ['FLASK_ENV'] == "testing":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
else: 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'

db.drop_all()
db.create_all()

Post.query.delete()
User.query.delete()

new_user_1 = User(first_name="Vera", last_name="Nouaime")
new_user_2 = User(first_name="John", last_name="Smith")
new_user_3 = User(first_name="Susie", last_name="Sal")
#adding user 4 in test cases
new_user_5 = User(first_name="Alice", last_name="Disney")

db.session.add_all([new_user_1, new_user_2, new_user_3, new_user_5])
db.session.commit()

# Posts for Vera
user_1_post_1 = Post(title="First Post", content="This is my first post!", created_at=datetime.now(), user_FK=new_user_1.id)
user_1_post_2 = Post(title="Second Post", content="This is my second post!", created_at=datetime.now(), user_FK=new_user_1.id)
user_1_post_3 = Post(title="Third Post", content="This is my third post!", created_at=datetime.now(), user_FK=new_user_1.id)

# Posts for John
user_2_post_1 = Post(title="Hello World", content="World!!!!!!!", created_at=datetime.now(), user_FK=new_user_2.id)
user_2_post_2 = Post(title="Olympics", content="Summer 2016", created_at=datetime.now(), user_FK=new_user_2.id)
user_2_post_3 = Post(title="Food", content="My favorite food is pizza!!!", created_at=datetime.now(), user_FK=new_user_2.id)

# Posts for Susie
user_3_post_1 = Post(title="Dogs", content="Black Labs", created_at=datetime.now(), user_FK=new_user_3.id)
user_3_post_2 = Post(title="Horses", content="They are so cute!", created_at=datetime.now(), user_FK=new_user_3.id)
user_3_post_3 = Post(title="Cats", content="Fluffy cat :)", created_at=datetime.now(), user_FK=new_user_3.id)
user_3_post_4 = Post(title="Fourth Post", content="This is my fourth post!", created_at=datetime.now(), user_FK=new_user_3.id)

db.session.add_all([
    user_1_post_1,
    user_1_post_2,
    user_1_post_3,
    user_2_post_1,
    user_2_post_2,
    user_2_post_3,
    user_3_post_1,
    user_3_post_2,
    user_3_post_3,
    user_3_post_4
]) 
db.session.commit()

# Tags 
tag_1 = Tag(name="New")
tag_2 = Tag(name="Exciting")
tag_3 = Tag(name="Cute")

db.session.add_all([tag_1, tag_2, tag_3])
db.session.commit()

# Adding Tags to Posts by appending them with M2M relationships established in models.py
user_1_post_1.tags.append(tag_1)
user_2_post_1.tags.append(tag_1)
user_3_post_1.tags.append(tag_1)

user_1_post_2.tags.append(tag_2)
user_2_post_2.tags.append(tag_2)
user_3_post_2.tags.append(tag_2)

user_1_post_3.tags.append(tag_3)
user_2_post_3.tags.append(tag_3)
user_3_post_3.tags.append(tag_3)

db.session.commit()


