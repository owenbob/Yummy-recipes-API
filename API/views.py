from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import jwt 
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

        return jsonify({"message ":"Invalid Data Submitted"})

    user_info = request.get_json(force=True)
    if user_info:
        hashed_password = generate_password_hash(user_info["password"], method="sha256")

        new_user = User(username=user_info["username"], email=user_info["email"], password=hashed_password)

        
        email_already_exists = db.session.query(db.exists().where(User.email == user_info["email"])).scalar()
        if email_already_exists:
            return jsonify({"message":"This email has already been used to register"})
        
        if user_info["username"] == "" or user_info["email"]== "" or user_info["password"]== "":
            return jsonify({"message":"Please ensure you have input all your details"})

        if  not validate_email(user_info["email"]):
            return jsonify({"message":"Please input correct email"})

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message" : "New user  has been created!"})

  

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

#Endpoint to create category
@app.route("/create_category", methods=["POST"])
@token_needed
def create_category(current_user):
    if not request.json:
        return jsonify({"message ":"Invalid Data Submitted"})
    
    data = request.get_json()

    new_category = Category(
        category_id=str(uuid.uuid4()),
        category_title=data["category_title"],
        category_description=data["category_description"],
        email=current_user.email
    )
    if data["category_title"]=="" or data["category_description"]== "":
        return jsonify({"message":"Please ensure that you have input a category title and description"})

    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message" : "Category created!"})




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
                output.append(category_data)

            return jsonify({"Categories" : output})
        

    if limit:
        paginate_categories = Category.query.filter_by(email=current_user.email).paginate(page, limit, False).items
        for category in paginate_categories:
            category_data = {}
            category_data["category_id"] = category.category_id
            category_data["category_title"] = category.category_title
            category_data["category_description"] = category.category_description
            output.append(category_data)

        return jsonify({"Categories" : output})
               
    else:
        categories = Category.query.filter_by(email=current_user.email).all()
        for category in categories:
            category_data = {}
            category_data["category_id"] = category.category_id
            category_data["category_title"] = category.category_title
            category_data["category_description"] = category.category_description
            output.append(category_data)

        return jsonify({"Categories" : output})



@app.route("/category/<category_id>", methods=["GET"])
@token_needed
def get_one_category(current_user, category_id):
    category= Category.query.filter_by(category_id=category_id, email=current_user.email).first()

    if not category:
        return jsonify({"message" : "No Category found!"})

    category_data = {}
    category_data["category_id"] = category.category_id
    category_data["category_title"] = category.category_title
    category_data["category_description"] = category.category_description

    return jsonify(category_data)


@app.route("/edit_category/<category_id>", methods=["PUT"])
@token_needed
def edit_category(current_user, category_id):
    category = Category.query.filter_by(category_id=category_id, email=current_user.email).first()

    if not  category:
        return jsonify({"message" : "No Category found!"})
    if not request.json:
        return jsonify({"message ":"Invalid Data Submitted"})

    data = request.get_json()
    if data["category_description"] == "":
        return jsonify({"message":"Please ensure that you have input a category description"})
    category.category_title = data["category_title"]
    category.category_description=data["category_description"]
    db.session.commit()

    return jsonify({"message" : "Category has been edited!"})


@app.route("/delete_category/<category_id>", methods=["DELETE"])
@token_needed
def delete_category(current_user, category_id):
    category = Category.query.filter_by(category_id=category_id, email=current_user.email).first()

    if not category :
        return jsonify({"message" : "No Category found!"})

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message" : "Category deleted!"})



@app.route("/create_recipe/<category_id>", methods=["POST"])
@token_needed
def create_recipe(current_user,category_id):

    Available_category = Category.query.filter_by(category_id = category_id,email=current_user.email).first()
    if not  Available_category:
        return({"message":"Category not available"}), 
    if not request.json:
        return jsonify({"message ":"Invalid Data Submitted"})
    
    data = request.get_json()


    if  data["recipe_title"] == "" or data["recipe_description"] == "":
        return jsonify({
            "message":"Please ensure that you have input a recipe_title,recipe_description and category title"
            })

     

    new_recipe = Recipe(
        recipe_id=str(uuid.uuid4()),
        recipe_title=data["recipe_title"],
        category_id=category_id,
        recipe_description=data["recipe_description"],
        email=current_user.email)

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
        search_recipes = Recipe.query.filter(Recipe.recipe_title.ilike('%' + search + '%'))
        if search_recipes:
            for recipe in search_recipes:
                recipe_data = {}
                recipe_data["recipe_id"] = recipe.recipe_id
                recipe_data["recipe_title"] = recipe.recipe_title
                recipe_data["category_id"] =recipe.category_id
                recipe_data["recipe_description"] = recipe.recipe_description
                output.append(recipe_data)

            return jsonify({"Recipes" : output})
        

    if limit:
        paginate_recipes = Recipe.query.filter_by(email=current_user.email).paginate(page, limit, False).items
        for recipe in paginate_recipes:
            recipe_data = {}
            recipe_data["recipe_id"] = recipe.recipe_id
            recipe_data["recipe_title"] = recipe.recipe_title
            recipe_data["category_id"] =recipe.category_id
            recipe_data["recipe_description"] = recipe.recipe_description
            output.append(recipe_data)

        return jsonify({"Recipes" : output})
               
    else:
        recipes = Recipe.query.filter_by(email=current_user.email).all()
        for recipe in recipes:
            recipe_data = {}
            recipe_data["recipe_id"] = recipe.recipe_id
            recipe_data["recipe_title"] = recipe.recipe_title
            recipe_data["category_id"] =recipe.category_id
            recipe_data["recipe_description"] = recipe.recipe_description
            output.append(recipe_data)

        return jsonify({"Recipes" : output})



@app.route("/recipe/<recipe_id>", methods=["GET"])
@token_needed
def get_one_recipe(current_user, recipe_id):
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()

    if not recipe:
        return jsonify({"message" : "No Recipe found!"})

    recipe_data = {}
    recipe_data["recipe_id"] = recipe.recipe_id
    recipe_data["recipe_title"] = recipe.recipe_title
    recipe_data["category_id"] =recipe.category_id
    recipe_data["recipe_description"] = recipe.recipe_description

    return jsonify(recipe_data)


@app.route("/edit_recipe/<recipe_id>", methods=["PUT"])
@token_needed
def edit_recipe(current_user, recipe_id):
    recipe = Recipe.query.filter_by(recipe_id=recipe_id, email=current_user.email).first()

    if not  recipe:
        return jsonify({"message" : "No Recipe found!"})

    if not request.json:
        return jsonify({"message ":"Invalid Data Submitted"})
        
    data = request.get_json()
    recipe.recipe_title =data["recipe_title"]
    recipe.recipe_description=data["recipe_description"]
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

