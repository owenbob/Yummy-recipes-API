import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Category(BaseTestCase):
     #-----------------------CATEGORY ENDPOINT--------------------------------
    
    def test_post_at_category_endpoint(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_get_at_category_endpoint_(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/category/<category_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_get_at_category_endpoint_with_poor_spelling(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/Category/<category_id>")
        assert response.status=="404 NOT FOUND"

    def test_put_at_category_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_delete_at_category_endpoint(self):
        #Testing the recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_get_at_category_endpoint_with_authorisation(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status
        response = self.client.get(
            "/category/<category_id>",
            headers = self.headers, 
            content_type='application/json'
            )
        self.assertIn(
            "No Category found!",
            str(response.data)
            )
        assert response.status=="404 NOT FOUND"
       
    def test_get_at_category_endpoint_with_authorisation_and_wrong_category_id(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status but a message that recipe is NOT found
        response = self.client.post(
            "/create_category",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category)
            )
        
        response = self.client.get(
            "/category/3",
            headers = self.headers, 
            content_type='application/json'
            )
        self.assertIn("No Category found!",str(response.data))
        assert response.status=="404 NOT FOUND"


    
    def test_get_at_category_endpoint_with_authorisation_and_the_category_id(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status
        response = self.client.post(
            "/create_category",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category)
            )
        response = self.client.get(
            "/category/1",
            headers = self.headers, 
            content_type='application/json'
            )
        self.assertIn("First meal of the morning",str(response.data))
        assert response.status=="200 OK"

