"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, default_image, connect_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def home():
    """ Redirects user to all users page """

    return redirect("/users")

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
    return render_template("user_page.html", user=user)

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


    
