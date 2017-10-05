from unittest import TestCase
from API.app import User,Recipe, db, app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import json

class BaseTestCase(TestCase):
    # def create_app(self):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin@localhost:5432/test"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
        # 
        # return app
    def setUp(self):
        self.client = app.test_client()
        db.init_app(app)
        db.create_all()

        user = User("Judyj", "jackson12334@xample.com", "12345")
        
        #recipe= Recipe("1","Rolex","Obtain eggs","jackson@xample.com")

        db.session.add(user)
        db.session.commit()

        """self.user={"username":"Jackson","password":"123"}
        response =self.client.post(
            "/login",data=json.dumps(self.user),headers={"Content-Type":"application/json"}
        )

        self.token=json.loads(response.get_data())["token"]
        """

    def tearDown(self):
        #db.session.remove()
        db.drop_all()