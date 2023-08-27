"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def home():
    return "Hello!"