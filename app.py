"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    users = User.query.all()

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

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_page(user_id): 

    user = User.query.get_or_404(user_id)
    return render_template("user_page.html", user=user)