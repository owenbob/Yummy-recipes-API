from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import jwt 



app = Flask(__name__)

app.config["SECRET_KEY"] = "owenbob101"

#directing API to databse yummy_recipes
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin@localhost:5432/yummy_recipes"

db = SQLAlchemy(app)


#-----------------------------------------------SQLALCHEMY MODELS-----------------------------------------------------


#User Model in SQL
class User(db.Model):
    
    # __table__ = "Users"

    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(50))
    email = db.Column(db.String(60))
    password = db.Column(db.String(80))


    def __init__(self,username,email, password):
        #initiliazing User class constructor
        self.username=username
        self.email = email
        self.password = password


    def __repr__(self):
        #method to return user information when querying database
        return "<User: %s>" % self.email

    

class Recipe(db.Model):
    
    # __table__ = "Recipes"

    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(1000))
    id = db.Column(db.Integer)



    def __init__(self,recipe_id,title,user_id):
            #initiliazing User class constructor
        self.recipe_id=recipe_id
        self.title = title
        self.user_id = user_id


    def __repr__(self):
        #method for retuning data when querying database
        return "<Recipe: %s>" % self.title



#-----------------------------------------------ROUTES----------------------------------------------------

#
@app.route("")
def 

#
@app.route("")
def 

#
@app.route("")
def 

#
@app.route("")
def 


#
@app.route("")
def 


#
@app.route("")
def 


#
@app.route("")
def 




if __name__ == "__main__":
    app.run(debug=True)