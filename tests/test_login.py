import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Login(BaseTestCase):
    #-----------------------LOGIN ENDPOINT--------------------------------

    def test_post_at_login_endpoint(self):
        #Testing the login end point
        #If the method is a POST Method Should  be not be allowed 
        response = self.client.post("/login")
        assert response.status=="400 BAD REQUEST"

    def test_put_at_login_endpoint(self):
        #Testing the login end point
        #If the method is a PUT, Method Should  be not be  allowed
        response = self.client.put("/login")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_delete_at_login_endpoint(self):
        #Testing the login end point
        #If the method is a delete, Method Should  be  not be allowed 
        response = self.client.delete("/login")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_get_at_login_endpoint(self):
        #Testing the login end point
        #If the method is a GET Method Should  be allowed and receive a positive status code
        response = self.client.get("/login")
        assert response.status=="400 BAD REQUEST"

    def test_get_at_login_endpoint_with_poor_spelling(self):
        #Testing the login end point
        #If the method is a GET Method Should  be allowed and receive a positive status code
        response = self.client.get("/Login")
        assert response.status=="404 NOT FOUND"
        
    def test_get_at_login_endpoint_with_user_details_who_is_not_registered(self):  
        #Testing the login end point with user credential

        response = self.client.get(
            "/login",
            data=json.dumps(self.user),
            headers = self.headers
            )
        self.assertIn(
            "1.Could not verify",
            str(response.data)
            )
        assert response.status=="400 BAD REQUEST"