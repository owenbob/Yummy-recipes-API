
from flask_sqlalchemy import SQLAlchemy
from API import app



#directing API to databse yummy_recipes
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://yummyrecipes:admin@localhost:5432/yummy_recipes"

db = SQLAlchemy(app)


#-----------------------------------------------SQLALCHEMY MODELS-----------------------------------------------------


#User Model in SQL
class User(db.Model):
    
    # __table__ = "Users"

       
    username = db.Column(db.String(50))
    email = db.Column(db.String(60),primary_key=True)
    password = db.Column(db.String(80))
    


    def __init__(self,username,email, password):
        #initiliazing User class constructor
        self.username=username
        self.email = email
        self.password = password

         
        


    def __repr__(self):
        #method to return user information when querying database
        return "<User: %s>" % self.email


class Category(db.Model):
    
    __tablename__ = "category"

    category_id = db.Column(db.String(100), primary_key=True)
    category_title = db.Column(db.String(30))
    category_description = db.Column(db.String(1000))
    email = db.Column(db.String(60))



    def __init__(self, category_id,category_title, category_description, email):
        #initiliazing recipe class constructor
        self.category_id=category_id
        self.category_title = category_title
        self.category_description = category_description
        self.email= email
       


    def __repr__(self):
        #method for returning data when querying database
        return "<Category: %s>" % self.category_title

    

class Recipe(db.Model):
    
    __tablename__ = "Recipes"

    recipe_id = db.Column(db.String(100), primary_key=True,)
    recipe_title = db.Column(db.String(30))
    recipe_description = db.Column(db.String(1000))
    category_id = db.Column(db.String(100),db.ForeignKey('category.category_id'))
    category = db.relationship('Category',backref=db.backref('recipe', lazy=True))
    email = db.Column(db.String(60))
    

    def __init__(self, recipe_id, recipe_title,recipe_description,category_id,email):
        #initiliazing recipe class constructor
        self.recipe_id= recipe_id
        self.recipe_title = recipe_title
        self.recipe_description= recipe_description
        self.category_id =category_id
        self.email= email
       


    def __repr__(self):
        #method for returning data when querying database
        return "<Recipe: %s>" % self.recipe_title
