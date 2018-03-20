"""Declaring these in the __init__.py ensures that they are global
and the necessary modules can access them.
"""
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)

# configuring app secret key
app.config["SECRET_KEY"] = "********"

# directing API to databse yummy_recipes
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://yummyrecipes:admin@localhost:5432/yummy_recipes" or os.environ.get('DATABASE_URL')

from API import views, models