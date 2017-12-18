
from flask_sqlalchemy import SQLAlchemy
from API import app


db = SQLAlchemy(app)

#-----------------------------------------------SQLALCHEMY MODELS-----------------------------------------------------
#User Model in SQL
class User(db.Model):
    
    username = db.Column(db.String(50))
    email = db.Column(db.String(60),primary_key=True)
    password = db.Column(db.String(80))
    user_date_stamp =db.Column(db.String(30))
    
    def __init__(self,username,email, password,user_date_stamp):
        #initiliazing User class constructor
        self.username=username
        self.email = email
        self.password = password
        self.user_date_stamp = user_date_stamp

    def __repr__(self):
        #method to return user information when querying database
        return "<User: %s>" % self.email


class Category(db.Model):
    
    __tablename__ = "category"

    category_id = db.Column(db.String(100), primary_key=True)
    category_title = db.Column(db.String(30))
    category_description = db.Column(db.String(1000))
    email = db.Column(db.String(60))
    category_date_stamp = db.Column(db.String(30))

    def __init__(self, category_id,category_title, category_description, email,category_date_stamp):
        #initiliazing recipe class constructor
        self.category_id = category_id
        self.category_title = category_title
        self.category_description = category_description
        self.email = email
        self.category_date_stamp = category_date_stamp
       
    def __repr__(self):
        #method for returning data when querying database
        return "<Category: %s>" % self.category_title

    

class Recipe(db.Model):
    
    __tablename__ = "Recipes"

    recipe_id = db.Column(db.String(100), primary_key=True)
    recipe_title = db.Column(db.String(30))
    recipe_description = db.Column(db.String(1000))
    category_id = db.Column(db.String(100),db.ForeignKey('category.category_id'))
    category = db.relationship('Category',backref=db.backref('recipe', lazy=True))
    email = db.Column(db.String(60))
    recipe_date_stamp = db.Column(db.String(30))
    recipe_public_status = db.Column(db.Boolean)
    
    def __init__(self, recipe_id, recipe_title,recipe_description,category_id,email,recipe_date_stamp,recipe_public_status):
        #initiliazing recipe class constructor
        self.recipe_id= recipe_id
        self.recipe_title = recipe_title
        self.recipe_description= recipe_description
        self.category_id =category_id
        self.email= email
        self.recipe_date_stamp = recipe_date_stamp
        self.recipe_public_status = recipe_public_status

    def __repr__(self):
        #method for returning data when querying database
        return "<Recipe: %s>" % self.recipe_title
