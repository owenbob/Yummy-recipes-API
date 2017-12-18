from flask import request,jsonify,make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from validate_email import validate_email
import datetime
import jwt 
import re
import uuid

from API import app
from API.models import User,Category,Recipe
from API.models import db




#Route for registering a user.This route takes the users details and assigns them a unique id 
@app.route("/register",methods=["POST"])
def create_user():
    
    if not request.json:

        return jsonify({
            "Status":"Fail",
            "message ":"Invalid Data Submitted"
            }),400

    user_info = request.get_json()
    username =user_info.get("username")
    email =user_info.get("email")
    password =user_info.get("password")

    #Checking if all fields are filled.
    if   isinstance(username,int):
        return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have input String"
            }),400

    #Checking if all fields are filled.
    if  not (username and  email and  password):
            return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have input all the required fields"
            }),400

    #Checking to see if the email is valid
    if  not validate_email(email):
        return jsonify({
            "Status":"Fail",
            "message":"Please input correct email"
            }),400
    
    #Checking for Special character in the name and email
    if  not re.match(
        "^[A-Za-z0-9_-]*$", 
        username) or  not re.match(
        "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", 
        email):
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure you have not input special characters"
        }),400

     #Checking if email already exists   
    email_already_exists = db.session.query(db.exists().where(User.email == email)).scalar()
    if email_already_exists:
        return jsonify({
            "Status":"Fail",
            "message":"This email has already been used to register"
            }),400
    #Checking to make sure no empty strings are sent
    if username == "" or email == "" or password== "":
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure you have input all your details"
            }),400
            
    hashed_password = generate_password_hash(password, method="sha256")
    new_user = User(
            username=username, 
            email=email, 
            password=hashed_password,
            user_date_stamp = str(datetime.datetime.now())
            )
    #Saving new user
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "New user  has been created!"
        }),201

#Method to assign token to function
def token_needed(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if not token:
            return jsonify({
                "message" : "1.Token is missing!"
                }), 401
        try: 
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(email=data["email"]).first()
        except:
            return jsonify({
                "Status":"Fail",
                "message" : "2.Token is invalid!"
                }), 401

        return f(current_user, *args, **kwargs)
    return decorated

  #Route to login and generate token   
@app.route("/login",methods=["POST","GET"])
def login():
    #Obtain user details in Json Format
    auth = request.get_json()
    if not auth or not auth["username"] or not auth["password"]:
        return  make_response(
            "1.Could not verify"
            ),400

    #Check Database to see if username provided is there
    user = User.query.filter_by(username=auth["username"]).first()

    if not user:
        return make_response(
            "2.Could not verify because provided details are not for user"
            ),400
    #Check the provided password and if true provide token
    if check_password_hash(user.password, auth["password"]):
        token = jwt.encode({
            "email" : user.email, 
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=50)}, 
            app.config["SECRET_KEY"])
        return jsonify({"token" : token.decode("UTF-8")}),201
    return make_response(
        "1.Could not verify"
        ),400

#Endpoint to create category
@app.route("/create_category", methods=["POST"])
@token_needed
def create_category(current_user):
    if not request.json:
        return jsonify({
            "Status":"Fail",
            "message ":"Invalid Data Submitted"
            }),400
    #Obtain data from user
    data = request.get_json()
    category_title = data.get("category_title")
    category_description = data.get("category_description")

    titlecase_category = title_case(category_title)
    
    #Checking if category already exists
    category_already_exists = db.session.query(db.exists().where(Category.category_title == titlecase_category)).scalar()
    if category_already_exists:
        return jsonify({
            "Status":"Fail",
            "message":"This category already exists"
            }),400

    #Check if all fields are filled
    if  not (category_title and category_description):
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure that you have input all the fields"
            }),400
    
    #Check to make sure there is no empty string
    if category_title == "" or category_description == "":
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure that you have input a category title and description"
            }),400


    new_category = Category(
        category_id = str(uuid.uuid4()),
        category_title = title_case(category_title),
        category_description = category_description,
        email = current_user.email,
        category_date_stamp = str(datetime.datetime.now())
    )

    #Save new category in the database
    db.session.add(new_category)
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "Category created!"
        }),201
        

#Route to get all categories
@app.route("/categories", methods=["GET"])
@token_needed
def get_all_categories(current_user):
    output = []
    search = request.args.get("q")
    limit = request.args.get('limit', None, type=int)
    page = request.args.get('page', 1, type=int)

    # If statement to  search categories by name
    if search:
        search_categories = Category.query.filter(Category.category_title.ilike('%' + search + '%'))
        if search_categories:
            for category in search_categories:
                category_data = {}
                category_data["category_id"] = category.category_id
                category_data["category_title"] = category.category_title
                category_data["category_description"] = category.category_description
                category_data["Category_date_stamp"] = category.category_date_stamp
                output.append(category_data)

            return jsonify({
                "Status":"Success",
                "Categories" : output
                }),200
     
    #If statement to handle pagination 
    if limit:
        paginate_categories = Category.query.filter_by(email=current_user.email).paginate(page, limit, False).items
        if paginate_categories:
            for category in paginate_categories:
                category_data = {}
                category_data["category_id"] = category.category_id
                category_data["category_title"] = category.category_title
                category_data["category_description"] = category.category_description
                category_data["Category_date_stamp"] = category.category_date_stamp
                output.append(category_data)

            return jsonify({
                "Status":"Success",
                "Categories" : output
                }),200
        else:
            return jsonify({
                "Status":"Fail",
                "Message" : " 404-Page Not Found"
                }),404
    #statement to handle return of all categories        
    else:
        categories = Category.query.filter_by(email=current_user.email).all()
        for category in categories:
            category_data = {}
            category_data["category_id"] = category.category_id
            category_data["category_title"] = category.category_title
            category_data["category_description"] = category.category_description
            category_data["Category_date_stamp"] = category.category_date_stamp
            output.append(category_data)

        return jsonify({
            "Status":"Success",
            "Categories" : output
            }),200

#Returning one category by its  category id
@app.route("/category/<category_id>", methods=["GET"])
@token_needed
def get_one_category(current_user, category_id):
    category= Category.query.filter_by(category_id=category_id, email=current_user.email).first()

    if not category:
        return jsonify({
            "Status":"Fail",
            "message" : "No Category found!"
            }),404

    category_data = {}
    category_data["category_id"] = category.category_id
    category_data["category_title"] = category.category_title
    category_data["category_description"] = category.category_description
    category_data["Category_date_stamp"] = category.category_date_stamp

    return jsonify(category_data)

#Endpoint to edit a category ie new category title and category description
@app.route("/edit_category/<category_id>", methods=["PUT"])
@token_needed
def edit_category(current_user, category_id):
    category = Category.query.filter_by(category_id=category_id, email=current_user.email).first()
    #Checking if it is a category
    if not  category:
        return jsonify({
        "Status":"Fail",
        "message" : "No Category found!"
        }),404
    #Checking if it a json object
    if not request.json:
        return jsonify({
            "Status":"Fail",
            "message ":"Invalid Data Submitted"
            }),400

    data = request.get_json()
    category_title=data.get("category_title")
    category_description=data.get("category_description")
    #Checking that all fields are filled
    if  not (category_title and category_description):
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure that you have input all the fields"
            }),400
    #Checking to make sure that there are no empty strings
    if category_title == "" or category_description == "":
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure that you have input a category  title and description"
            }),400
   
    #Replacing the old values in the databse with the new inputs
    category.category_title = category_title
    category.category_description=category_description
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "Category has been edited!"
        }),201

#Delete endpoint
@app.route("/delete_category/<category_id>", methods=["DELETE"])
@token_needed
def delete_category(current_user, category_id):
    category = Category.query.filter_by(category_id=category_id, email=current_user.email).first()

    if not category :
        return jsonify({
            "Status":"Fail",
            "message" : "No Category found!"
            }),404
    #deleting from the database
    db.session.delete(category)
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "Category deleted!"
        }),200

#Endpoint to create recipes using a valid category id
@app.route("/create_recipe/<category_id>", methods=["POST"])
@token_needed
def create_recipe(current_user,category_id):

    #Querying to see if the category exists
    Available_category = Category.query.filter_by(category_id = category_id,email=current_user.email).first()
    if not  Available_category:
        return({
            "Status":"Fail",
            "message":"Category not available"
            }),400
    #checking if its a json object
    if not request.json:
        return jsonify({
            "Status":"Fail",
            "message ":"Invalid Data Submitted"
            }),400
    #Obtaining data 
    data = request.get_json()
    recipe_title =data.get("recipe_title")
    recipe_description=data.get("recipe_description")

    #Checking to see if all fields are filled
    if  not (recipe_title and recipe_description):
        return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have all fields"
            }),400

    #Checking to make sure there is no empty string
    if  recipe_title == "" or recipe_description == "":
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure that you have input a recipe_title and recipe_description "
            }),400

    new_recipe = Recipe(
        recipe_id=str(uuid.uuid4()),
        recipe_title=data["recipe_title"],
        category_id=category_id,
        recipe_description=data["recipe_description"],
        recipe_public_status = False,
        email=current_user.email,
        recipe_date_stamp = str(datetime.datetime.now())
        )

    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "Recipe created!"
        }),201

#Route to get all Recipes
@app.route("/recipes", methods=["GET"])
@token_needed
def get_all_recipes(current_user):
    output = []
    search = request.args.get("q")
    limit = request.args.get('limit', None, type=int)
    page = request.args.get('page', 1, type=int)
    #Searching for a recipe using the recipe name
    if search:
        search_recipes = Recipe.query.filter(Recipe.recipe_title.ilike('%' + search + '%'))
        if search_recipes:
            for recipe in search_recipes:
                category = Category.query.filter_by(category_id=recipe.category_id, email=current_user.email).first()
                recipe_data = {}
                recipe_data["recipe_id"] = recipe.recipe_id
                recipe_data["recipe_title"] = recipe.recipe_title
                recipe_data["category_id"] =recipe.category_id
                recipe_data["category_title"] = category.category_title
                recipe_data["category_description"] = category.category_description
                recipe_data["category_date_stamp"] = category.category_date_stamp
                recipe_data["recipe_description"] = recipe.recipe_description
                recipe_data["recipe_date_stamp"] = recipe.recipe_date_stamp
                recipe_data ["recipe_public_status"] = recipe.recipe_public_status
                output.append(recipe_data)

            return jsonify({
                "Status":"Success",
                "Recipes" : output
                }),200

    #If statement to handle pagination 
    if limit:
        paginate_recipes = Recipe.query.filter_by(email=current_user.email).paginate(page, limit, False).items
        if pagoinate_recipes:
            for recipe in paginate_recipes:
                category = Category.query.filter_by(category_id=recipe.category_id, email=current_user.email).first()
                recipe_data = {}
                recipe_data["recipe_id"] = recipe.recipe_id
                recipe_data["recipe_title"] = recipe.recipe_title
                recipe_data["category_id"] =recipe.category_id
                recipe_data["category_title"] = category.category_title
                recipe_data["category_description"] = category.category_description
                recipe_data["category_date_stamp"] = category.category_date_stamp
                recipe_data["recipe_description"] = recipe.recipe_description
                recipe_data["recipe_date_stamp"] = recipe.recipe_date_stamp
                recipe_data ["recipe_public_status"] = recipe.recipe_public_status
                output.append(recipe_data)
                output.append(recipe_data)

            return jsonify({
                "Status":"Success",
                "Recipes" : output
                }),200
        else:
            return jsonify({
                "Status":"Success",
                "Messages" : "404-Page Not Found"
                }),404
    #Statement to get all recipes          
    else:
        recipes = Recipe.query.filter_by(email=current_user.email).all()
        for recipe in recipes:
            category = Category.query.filter_by(category_id=recipe.category_id, email=current_user.email).first()

            recipe_data = {}
            recipe_data["recipe_id"] = recipe.recipe_id
            recipe_data["recipe_title"] = recipe.recipe_title
            recipe_data["category_id"] =recipe.category_id
            recipe_data["category_title"] = category.category_title
            recipe_data["category_description"] = category.category_description
            recipe_data["category_date_stamp"] = category.category_date_stamp
            recipe_data["recipe_description"] = recipe.recipe_description
            recipe_data["recipe_date_stamp"] = recipe.recipe_date_stamp
            recipe_data ["recipe_public_status"] = recipe.recipe_public_status
            output.append(recipe_data)

        return jsonify({
            "Status":"Success",
            "Recipes" : output
            }),200

#Obtaing a reciep by recipe id
@app.route("/recipe/<recipe_id>", methods=["GET"])
@token_needed
def get_one_recipe(current_user, recipe_id):
    #Checking to see if its a recipe and is in the database
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()
    
    if not recipe:
        return jsonify({
            "Status":"Fail",
            "message" : "No Recipe found!"
            }),404

    category = Category.query.filter_by(category_id=recipe.category_id, email=current_user.email).first() 
    recipe_data = {}
    recipe_data["recipe_id"] = recipe.recipe_id
    recipe_data["recipe_title"] = recipe.recipe_title
    recipe_data["category_id"] =recipe.category_id
    recipe_data["category_title"] = category.category_title
    recipe_data["category_description"] = category.category_description
    recipe_data["Category_date_stamp"] = category.category_date_stamp
    recipe_data["recipe_description"] = recipe.recipe_description
    recipe_data["recipe_date_stamp"] = recipe.recipe_date_stamp
    recipe_data ["recipe_public_status"] = recipe.recipe_public_status

    return jsonify(recipe_data)

#Endpoint to edit recipe using a specific id
@app.route("/edit_recipe/<recipe_id>", methods=["PUT"])
@token_needed
def edit_recipe(current_user, recipe_id):
    #Checking to see if its a recipe and is in the database
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()

    if not  recipe:
        return jsonify({
        "Status":"Fail",
        "message" : "No Recipe found!"
        }),404
    #Checking if its a json object
    if not request.json:
        return jsonify({
            "Status":"Fail",
            "message ":"Invalid Data Submitted"
            }),400
     #Obtaining data from user    
    data = request.get_json()
    recipe_title = data.get("recipe_title")
    recipe_description = data.get("recipe_description")

    #Checking to see if all fields are filled.
    if not (recipe_title and recipe_description):
        return jsonify({
            "Status":"Fail",
        "message" : "Please ensure all fields are filled!"
        }),400

    recipe.recipe_title =recipe_title
    recipe.recipe_description=recipe_description
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "Recipe has been edited!"
        }),201

#Route to set recipe status to public so that it can be displayed on the home page
@app.route("/set_public_recipe/<recipe_id>",methods=["PATCH"])
@token_needed
def set_public_recipe(current_user,recipe_id):
    #Querying the database to see if the recipe exists 
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()

    if not recipe:
        return jsonify({
            "Status":"Fail",
            "message" : "No Recipe found!"
            }),404

    recipe.recipe_public_status = True
    db.session.commit()
    return jsonify({
        "Status":"Success",
        "message" : "Recipe is now Public!"
        }),201

#route to delete recipe from database 
@app.route("/delete_recipe/<recipe_id>", methods=["DELETE"])
@token_needed
def delete_recipe(current_user, recipe_id):
    #Querying the database to see if the recipe exists 
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()

    if not recipe:
        return jsonify({
            "Status":"Fail",
            "message" : "No Recipe found!"
            }),404

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "Recipe deleted!"
        }),200

#Route to display public recipes
@app.route("/home",methods=["GET"])
def public_recipes():
    output=[]
    ##Querying the database to see if the recipe exists 
    recipes = Recipe.query.filter_by(recipe_public_status=True).all()

    for recipe in recipes:
        category = Category.query.filter_by(category_id=recipe.category_id).first()

        recipe_data = {}
        recipe_data["recipe_id"] = recipe.recipe_id
        recipe_data["recipe_title"] = recipe.recipe_title
        recipe_data["category_id"] =recipe.category_id
        recipe_data["category_title"] = category.category_title
        recipe_data["category_description"] = category.category_description
        recipe_data["category_date_stamp"] = category.category_date_stamp
        recipe_data["recipe_description"] = recipe.recipe_description
        recipe_data["recipe_date_stamp"] = recipe.recipe_date_stamp
        recipe_data["recipe_public_status"] = recipe.recipe_public_status
        output.append(recipe_data)

    return jsonify({
        "Status":"Success",
        "Recipes" : output
        }),200


def title_case(data):
    data = ' '.join(''.join([w[0].upper(), w[1:].lower()]) for w in data.split())
    return data

