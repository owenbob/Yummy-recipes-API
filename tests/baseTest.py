from unittest import TestCase
from API.app import User,Recipe, db, app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

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

        user = User("Judy", "judy@example.com", "123")
        #recipe=Recipe

        db.session.add(user)
        db.session.commit()


    def tearDown(self):
        db.drop_all()