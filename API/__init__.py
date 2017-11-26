import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)

app.config["SECRET_KEY"] = "********"

#directing API to databse yummy_recipes
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://yummyrecipes:admin@localhost:5432/yummy_recipes" or os.environ('DATABASE_URL')



from API import views,models