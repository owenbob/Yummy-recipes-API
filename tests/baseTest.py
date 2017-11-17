from unittest import TestCase
from API.app import User,Recipe, db, app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class BaseTestCase(TestCase):
    # def create_app(self):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://yummyrecipes:admin@localhost:5432/test"
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memory"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        # 
        # return app
    def setUp(self):
        

        self.client = app.test_client()
        db.init_app(app)
        db.drop_all()
        db.create_all()

        password="123"
        self.user = {"david","david@gmail.com",password}
        
        password_hash = generate_password_hash(password, method='sha256')
        user=User("david","david1@gmail.com",password=password_hash)

        db.session.add(user)
        db.session.commit()
        
        recipe_id=str(uuid.uuid4())
        self.recipe ={"rolex","1.Obtain eggs"}
        recipe=Recipe(recipe_id,"rolex","1.Obtain eggs","david@gmail.com")

        db.session.add(recipe)
        db.session.commit()
       

        self.user = {"username":"david","password": "123"}
        response = self.client.post("/login", data=json.dumps(self.user),headers={"Content-Type": "application/json"})
        token = json.loads(response.data.decode())["token"]

        self.headers= dict(token=token)
        

    def tearDown(self):
        db.session.remove()
        db.drop_all()

#if __name__ ==  "__main__":
    #unittest.main()    