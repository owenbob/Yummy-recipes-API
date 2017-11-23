from unittest import TestCase
from API.app import User,Category,Recipe, db, app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class BaseTestCase(TestCase):
    # def create_app(self):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://yummyrecipes:admin@localhost:5432/test"
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    def setUp(self):
        

        self.client = app.test_client()
        db.init_app(app)
        db.drop_all()
        db.create_all()

        password="123"
        self.user = {"david","david@gmail.com",password}
        
        password_hash = generate_password_hash(password, method='sha256')
        user=User("david","david@gmail.com",password=password_hash)

        db.session.add(user)
        db.session.commit()

        self.invalid_data = {}
        #self.incomplete_user = {"","david@gmail.com",password}
        #self.invalid_email_user = {"red","dwrndgmail.com",password}
        #self.user2 = {"Jackson","david@gmail.com","password"}

        
        self.category = {
            "category_title":"breakfast",
            "category_description":"First meal of the morning"
        }
        category=Category("1","breakfast","First meal of the morning","david@gmail.com")

        db.session.add(category)
        db.session.commit()

        
        
        
        self.recipe ={
            "recipe_title":"rolex", 
            "recipe_description":"1.Obtain eggs"
            }
        recipe=Recipe("1","rolex","1.Obtain eggs","1","david@gmail.com")

        db.session.add(recipe)
        db.session.commit()
       
        
        self.user = {"username":"david","password": "123"}
        response = self.client.post("/login", data=json.dumps(self.user),headers={"Content-Type": "application/json"})
        token = json.loads(response.data.decode())["token"]

        self.headers= {"x-access-token": token}
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()

#if __name__ ==  "__main__":
    #unittest.main()    