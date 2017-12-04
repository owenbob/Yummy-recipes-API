from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt 
import re
from functools import wraps
import uuid
from validate_email import validate_email
from API import app
from API.models import db
from flask import request,jsonify,make_response
from API.models import User,Category,Recipe




#Route for registering a user.This route takes the users details and assigns them a unique id
@app.route("/register",methods=["POST"])
def create_user():
    
    if not request.json:

        return jsonify({
            "Status":"Fail",
            "message ":"Invalid Data Submitted"
            }),400

    user_info = request.get_json(force=True)
    
    if user_info:
        hashed_password = generate_password_hash(user_info["password"], method="sha256")

        new_user = User(
            username=user_info["username"], 
            email=user_info["email"], 
            password=hashed_password,
            user_date_stamp = str(datetime.datetime.now())
            )
        
        if  not re.match(
            "^[A-Za-z0-9_-]*$", 
            user_info['username']) or  not re.match(
            "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", 
            user_info['email']):
            return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have not input special characters"
            }),400
        email_already_exists = db.session.query(db.exists().where(User.email == user_info["email"])).scalar()
        if email_already_exists:
            return jsonify({
                "Status":"Fail",
                "message":"This email has already been used to register"
                }),400
        
        if user_info["username"] == "" or user_info["email"]== "" or user_info["password"]== "":
            return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have input all your details"
                }),400

        if  not validate_email(user_info["email"]):
            return jsonify({
                "Status":"Fail",
                "message":"Please input correct email"
                }),400

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
    #auth = request.authorization
    auth = request.get_json()

    if not auth or not auth["username"] or not auth["password"]:
        return  make_response(
            "1.Could not verify"
            ),400

    user = User.query.filter_by(username=auth["username"]).first()

    if not user:
        return make_response(
            "2.Could not verify because provided details are not for user"
            ),400

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
    
    data = request.get_json()

    new_category = Category(
        category_id=str(uuid.uuid4()),
        category_title=data["category_title"],
        category_description=data["category_description"],
        email=current_user.email,
        category_date_stamp =str(datetime.datetime.now())
    )
    if  not re.match("^[A-Za-z0-9_-]*$", data["category_title"]) or  not re.match("^[A-Za-z0-9_-]*$", data["category_description"]):
            return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have not input special characters"
            }),400

    if data["category_title"]=="" or data["category_description"]== "":
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure that you have input a category title and description"
            }),400

    db.session.add(new_category)
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "Category created!"
        }),201




#Route to get all Recipes
@app.route("/categories", methods=["GET"])
@token_needed
def get_all_categories(current_user):
    output = []
    search = request.args.get("q")
    limit = request.args.get('limit', None, type=int)
    page = request.args.get('page', 1, type=int)

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
        

    if limit:
        paginate_categories = Category.query.filter_by(email=current_user.email).paginate(page, limit, False).items
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


@app.route("/edit_category/<category_id>", methods=["PUT"])
@token_needed
def edit_category(current_user, category_id):
    category = Category.query.filter_by(category_id=category_id, email=current_user.email).first()

    if not  category:
        return jsonify({
        "Status":"Fail",
        "message" : "No Category found!"
        }),404

    if not request.json:
        return jsonify({
            "Status":"Fail",
            "message ":"Invalid Data Submitted"
            }),400

    data = request.get_json()
    if data["category_title"] or data["category_description"] == "":
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure that you have input a category description"
            }),400
    if  not re.match("^[A-Za-z0-9_-]*$", data["category_title"]) or  not re.match("^[A-Za-z0-9_-]*$", data["category_description"]):
            return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have not input special characters"
            }),400

    category.category_title = data["category_title"]
    category.category_description=data["category_description"]
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "Category has been edited!"
        }),201


@app.route("/delete_category/<category_id>", methods=["DELETE"])
@token_needed
def delete_category(current_user, category_id):
    category = Category.query.filter_by(category_id=category_id, email=current_user.email).first()

    if not category :
        return jsonify({
            "Status":"Fail",
            "message" : "No Category found!"
            }),404

    db.session.delete(category)
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "Category deleted!"
        }),200



@app.route("/create_recipe/<category_id>", methods=["POST"])
@token_needed
def create_recipe(current_user,category_id):

    Available_category = Category.query.filter_by(category_id = category_id,email=current_user.email).first()
    if not  Available_category:
        return({
            "Status":"Fail",
            "message":"Category not available"
            }),400
    if not request.json:
        return jsonify({
            "Status":"Fail",
            "message ":"Invalid Data Submitted"
            }),400
    
    data = request.get_json()
    if  not re.match("^[A-Za-z0-9_-]*$", data["recipe_title"]) or  not re.match("^[A-Za-z0-9_-]*$", data["recipe_description"]):
            return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have not input special characters"
            }),400


    if  data["recipe_title"] == "" or data["recipe_description"] == "":
        return jsonify({
            "Status":"Fail",
            "message":"Please ensure that you have input a recipe_title,recipe_description and category title"
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

    if search:
        search_recipes = Recipe.query.filter(Recipe.recipe_title.ilike('%' + search + '%'))
        if search_recipes:
            for recipe in search_recipes:
                recipe_data = {}
                recipe_data["recipe_id"] = recipe.recipe_id
                recipe_data["recipe_title"] = recipe.recipe_title
                recipe_data["category_id"] =recipe.category_id
                recipe_data["recipe_description"] = recipe.recipe_description
                recipe_data["recipe_date_stamp"] = recipe.recipe_date_stamp
                recipe_data["recipe_public_status"] = recipe.recipe_public_status
                output.append(recipe_data)

            return jsonify({
                "Status":"Success",
                "Recipes" : output
                }),200
        

    if limit:
        paginate_recipes = Recipe.query.filter_by(email=current_user.email).paginate(page, limit, False).items
        for recipe in paginate_recipes:
            recipe_data = {}
            recipe_data["recipe_id"] = recipe.recipe_id
            recipe_data["recipe_title"] = recipe.recipe_title
            recipe_data["category_id"] =recipe.category_id
            recipe_data["recipe_description"] = recipe.recipe_description
            recipe_data["recipe_date_stamp"] = recipe.recipe_date_stamp
            recipe_data["recipe_public_status"] = recipe.recipe_public_status
            output.append(recipe_data)

        return jsonify({
            "Status":"Success",
            "Recipes" : output
            }),200
               
    else:
        recipes = Recipe.query.filter_by(email=current_user.email).all()
        for recipe in recipes:
            recipe_data = {}
            recipe_data["recipe_id"] = recipe.recipe_id
            recipe_data["recipe_title"] = recipe.recipe_title
            recipe_data["category_id"] =recipe.category_id
            recipe_data["recipe_description"] = recipe.recipe_description
            recipe_data["recipe_date_stamp"] = recipe.recipe_date_stamp
            recipe_data["recipe_public_status"] = recipe.recipe_public_status
            output.append(recipe_data)

        return jsonify({
            "Status":"Success",
            "Recipes" : output
            }),200



@app.route("/recipe/<recipe_id>", methods=["GET"])
@token_needed
def get_one_recipe(current_user, recipe_id):
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()

    if not recipe:
        return jsonify({
            "Status":"Fail",
            "message" : "No Recipe found!"
            }),404

    recipe_data = {}
    recipe_data["recipe_id"] = recipe.recipe_id
    recipe_data["recipe_title"] = recipe.recipe_title
    recipe_data["category_id"] =recipe.category_id
    recipe_data["recipe_description"] = recipe.recipe_description
    recipe_data["recipe_date_stamp"] = recipe.recipe_date_stamp
    recipe_date["recipe_public_status"] = recipe.recipe_public_status

    return jsonify(recipe_data)


@app.route("/edit_recipe/<recipe_id>", methods=["PUT"])
@token_needed
def edit_recipe(current_user, recipe_id):
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()

    if not  recipe:
        return jsonify({
        "Status":"Fail",
        "message" : "No Recipe found!"
        }),404

    if not request.json:
        return jsonify({
            "Status":"Fail",
            "message ":"Invalid Data Submitted"
            }),400
        
    data = request.get_json()
    if  not re.match("^[A-Za-z0-9_-]*$", data["recipe_title"]) or  not re.match("^[A-Za-z0-9_-]*$", data["recipe_description"]):
            return jsonify({
                "Status":"Fail",
                "message":"Please ensure you have not input special characters"
            }),400
    recipe.recipe_title =data["recipe_title"]
    recipe.recipe_description=data["recipe_description"]
    
    db.session.commit()

    return jsonify({
        "Status":"Success",
        "message" : "Recipe has been edited!"
        }),201


@app.route("/set_public_recipe/<recipe_id>",methods=["PUT"])
@token_needed
def set_public_recipe(current_user,recipe_id):
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

@app.route("/delete_recipe/<recipe_id>", methods=["DELETE"])
@token_needed
def delete_recipe(current_user, recipe_id):
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


@app.route("/home",methods=["GET"])
def public_recipes():
    output=[]

    recipes = Recipe.query.filter_by(recipe_public_status=True).all()
    for recipe in recipes:
        recipe_data = {}
        recipe_data["recipe_id"] = recipe.recipe_id
        recipe_data["recipe_title"] = recipe.recipe_title
        recipe_data["category_id"] =recipe.category_id
        recipe_data["recipe_description"] = recipe.recipe_description
        recipe_data["recipe_date_stamp"] = recipe.recipe_date_stamp
        recipe_data["recipe_public_status"] = recipe.recipe_public_status
        output.append(recipe_data)

    return jsonify({
        "Status":"Success",
        "Recipes" : output
        }),200



