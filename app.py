"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, default_image, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def home():
    """ Redirects user to all users page """

    return redirect("/users")


# User Database routes

@app.route("/users")
def all_users(): 
    """ Displays list of all users """
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template("base.html", users=users)

@app.route("/users/new")
def users_new_form(): 
    """ Displays form to create a new user """

    return render_template("new_user_form.html")

@app.route("/users/new", methods=["POST"])
def users_new(): 
    """ Handles POST request for new user """ 

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url" or None]

    new_user = User(first_name=first_name, last_name=last_name)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_page(user_id): 
    """ Displays user page for primary key of user passed in through route """

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_FK=user.id)

    return render_template("user_page.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def user_edit(user_id): 
    """ Displays edit form for current user """

    user = User.query.get_or_404(user_id)

    return render_template("user_edit_form.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_edit_post(user_id): 
    """ Displays edit form for current user. If user, leaves first, last name, or
    image_url fields empty, default will be previous values stored in database. 
    If any changes are made, changes are saved to database """

    user = User.query.get_or_404(user_id)

    if request.form["first_name"]:
        user.first_name = request.form["first_name"]

    if request.form["last_name"]:
        user.last_name = request.form["last_name"]

    if request.form["image_url"]:
        user.image_url = request.form["image_url"]
    
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def user_delete(user_id): 
    """ Deletes existing user from database when button is clicked """
    
    user = User.query.get_or_404(user_id) 
    
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


# Post Database routes

@app.route("/users/<int:user_id>/posts/new")
def display_new_post_form(user_id):
    """ Displays form to create new post for user """
    
    user = User.query.get_or_404(user_id)

    return render_template("post_new_form.html", user=user)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_new_post(user_id):
    """ Handles POST request for new post of user """
    
    user = User.query.get_or_404(user_id)
    
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, created_at=datetime.now(), user_FK= user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/posts/<int:post_id>")
def display_post(post_id):
    """ Displays title, content, and author of post clicked. There is a 
    foreign key to user table """

    post = Post.query.get_or_404(post_id)

    return render_template("post_page.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def post_edit(post_id): 
    """ Displays edit form for clicked post """

    post = Post.query.get_or_404(post_id)

    return render_template("post_edit_form.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def post_edit_post(post_id): 
    """ Displays edit form for clicked post. If user, leaves title or
    content fields unchanged, default will be previous values stored in database. 
    If any changes are made, changes are saved to database """

    post = Post.query.get_or_404(post_id)

    if post.title != request.form["title"]:
        post.title = request.form["title"]

    if post.content != request.form["content"]:
        post.content = request.form["content"]
    
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def post_delete(post_id): 
    """ Deletes existing post from database when button is clicked """
    
    post = Post.query.get_or_404(post_id) 
    user = User.query.get_or_404(post.user.id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")



