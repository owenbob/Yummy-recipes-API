from flask import Flask,request,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt 
from functools import wraps
import uuid




app = Flask(__name__)

app.config["SECRET_KEY"] = "********"

#directing API to databse yummy_recipes
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin@localhost:5432/yummy_recipes"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://yummyrecipes:admin@localhost:5432/yummy_recipes"

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

    

class Recipe(db.Model):
    
    # __table__ = "Recipes"

    recipe_id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(1000))
    email = db.Column(db.String(60))
    



    def __init__(self, recipe_id, title, description, email):
        #initiliazing recipe class constructor
        self.recipe_id=recipe_id
        self.title = title
        self.description=description
        self.email= email
       


    def __repr__(self):
        #method for returning data when querying database
        return "<Recipe: %s>" % self.title



#-----------------------------------------------ROUTES/ENDPOINTS----------------------------------------------------

#Route for registering a user.This route takes the users details and assigns them a unique id
@app.route("/register",methods=["Post"])
def create_user():
    user_info = request.get_json(force=True)
    hashed_password = generate_password_hash(user_info["password"], method="sha256")

    new_user = User(username=user_info["username"], email=user_info["email"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message" : "New user  has been created!"})

   
"""   
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
        registered_users.append(user_data)

    return jsonify({"users" : registered_users})
    
#Route to obtain an individual user in the databse using their id
@app.route("/registered_user/<email>" ,methods=["GET"])
def get_user(email):
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message" : "No user found!"})

    user_data = {}
    user_data["username"] = user.username
    user_data["email"] =user.email
    user_data["password"] = user.password
    
    return jsonify({"user" : user_data})
 


#Route to delete an individual user using their email
@app.route("/delete_registered_user/<email>",methods=["DELETE"])
def delete_user(email):
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message" : "No user found!"})

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message" : "The user has been deleted!"})
"""
#Method to assign token to function
def token_needed(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return jsonify({"message" : "1.Token is missing!"}), 401

        try: 
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(email=data["email"]).first()
        except:
            return jsonify({"message" : "2.Token is invalid!"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


  #Route to login and generate token   
@app.route("/login",methods=["POST","GET"])
def login():
    #auth = request.authorization
    auth = request.get_json()

    if not auth or not auth["username"] or not auth["password"]:
        return  make_response("1.Could not verify")

    user = User.query.filter_by(username=auth["username"]).first()

    if not user:
        return make_response("2.Could not verify because provided details are not for user")

    if check_password_hash(user.password, auth["password"]):
        
        token = jwt.encode({"email" : user.email, "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=50)}, app.config["SECRET_KEY"])

        return jsonify({"token" : token.decode("UTF-8")})

    return make_response("1.Could not verify")


@app.route("/create_recipe", methods=["POST"])
@token_needed
def create_recipe(current_user):
    #data = request.get_json(force=True)
    #print("here")
    data = request.get_json()

    new_recipe = Recipe(recipe_id=str(uuid.uuid4()), title=data["title"],description=data["description"],email=current_user.email)
    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({"message" : "Recipe created!"})


#Route to get all Recipes
@app.route("/recipes", methods=["GET"])
@token_needed
def get_all_recipes(current_user):
    output = []
    search = request.args.get("q")
    limit = request.args.get('limit', None, type=int)
    page = request.args.get('page', 1, type=int)

    if search:
        search_recipes = Recipe.query.filter(Recipe.title.ilike('%' + search + '%'))
        if search_recipes:
            for recipe in search_recipes:
                recipe_data = {}
                recipe_data["recipe_id"] = recipe.recipe_id
                recipe_data["title"] = recipe.title
                recipe_data["description"] = recipe.description
                output.append(recipe_data)

            return jsonify({"Recipes" : output})
        

    if limit:
        paginate_recipes = Recipe.query.filter_by(email=current_user.email).paginate(page, limit, False).items
        for recipe in paginate_recipes:
            recipe_data = {}
            recipe_data["recipe_id"] = recipe.recipe_id
            recipe_data["title"] = recipe.title
            recipe_data["description"] = recipe.description
            output.append(recipe_data)

        return jsonify({"Recipes" : output})
               
    else:
        recipes = Recipe.query.filter_by(email=current_user.email).all()
        for recipe in recipes:
            recipe_data = {}
            recipe_data["recipe_id"] = recipe.recipe_id
            recipe_data["title"] = recipe.title
            recipe_data["description"] = recipe.description
            output.append(recipe_data)

        return jsonify({"Recipes" : output})



@app.route("/recipe/<recipe_id>", methods=["GET"])
@token_needed
def get_one_recipe(current_user, recipe_id):
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()

    if not recipe:
        return jsonify({"message" : "No Recipe found!"})
#recipe_id, title, description
    recipe_data = {}
    recipe_data["recipe_id"] = recipe.recipe_id
    recipe_data["title"] = recipe.title
    recipe_data["description"] = recipe.description

    return jsonify(recipe_data)


@app.route("/edit_recipe/<recipe_id>", methods=["PUT"])
@token_needed
def edit_recipe(current_user, recipe_id):
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()

    if not  recipe:
        return jsonify({"message" : "No Recipe found!"})
    data = request.get_json()
    recipe.description=data["description"]
    db.session.commit()

    return jsonify({"message" : "Recipe has been edited!"})

@app.route("/delete_recipe/<recipe_id>", methods=["DELETE"])
@token_needed
def delete_recipe(current_user, recipe_id):
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()

    if not recipe:
        return jsonify({"message" : "No Recipe found!"})

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({"message" : "Recipe deleted!"})

