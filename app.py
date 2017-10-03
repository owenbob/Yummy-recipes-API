from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

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

#Route for registering a user.This route takes the users details and assigns them a unique id
@app.route("/register",methods=["Post"])
def create_user():
    user_info = request.get_json()

    hashed_password = generate_password_hash(user_info["password"], method="sha256")

    new_user = User(username=user_info["username"], email=user_info["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message" : "New user  has been created!"})

#Route for obtaining all users in the database
@app.route("/registered_users",methods=["GET"])
def get_users():
    users = User.query.all()

    registered_users= []

    for user in users:
        user_data = {}
        user_data["username"] = user.username
        user_data["email"] = user.email
        user_data["password"] = user.password
        user_data["id"] = user.id
        registered_users.append(user_data)

    return jsonify({"users" : registered_users})
    
#Route to obtain an individual user in the databse using their id
@app.route("/registered_user/<int:id>" ,methods=["GET"])
def get_user(id):
    
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({"message" : "No user found!"})

    user_data = {}
    user_data["username"] = user.username
    user_data["email"] =user.email
    user_data["password"] = user.password
    user_data["id"] = user.id
    
    return jsonify({"user" : user_data})
 


#Route to delete an individual user using their id
@app.route("/delete_registered_user/<username>",methods=["DELETE"])
def delete_user(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message" : "No user found!"})

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message" : "The user has been deleted!"})
     

"""
# #
# @app.route("")
# def 


# #
# @app.route("")
# def 


# #
# @app.route("")
# def 

"""


if __name__ == "__main__":
    app.run(debug=True)