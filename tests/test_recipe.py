import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Recipe(BaseTestCase):
    #-----------------------RECIPE ENDPOINT--------------------------------
    
    def test_post_at_recipe_endpoint(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_get_at_recipe_endpoint_(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/recipe/<recipe_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_get_at_recipe_endpoint_with_poor_spelling(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/Recipe/<recipe_id>")
        assert response.status=="404 NOT FOUND"

    def test_put_at_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_delete_at_recipe_endpoint(self):
        #Testing the recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_get_at_recipe_endpoint_with_authorisation(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status
        response = self.client.get(
            "/recipe/<recipe_id>",
            headers = self.headers, 
            content_type='application/json'
            )
        assert response.status=="404 NOT FOUND"
    
    def test_get_at_recipe_endpoint_with_authorisation_and_wrong_recipe_id(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status but a message that recipe is NOT found
        response = self.client.post(
            "/create_recipe",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.recipe)
            )
        response = self.client.get("/recipe/4",
        headers = self.headers, 
        content_type='application/json'
        )
        self.assertIn(
            "No Recipe found!",
            str(response.data)
            )
        assert response.status=="404 NOT FOUND"
    
    
    def test_get_at_recipe_endpoint_with_authorisation_and_the_recipe_id(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status
        response = self.client.post(
            "/create_category",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category)
            )
        response = self.client.post(
            "/create_recipe/1",
            headers = self.headers,
             content_type='application/json', 
             data=json.dumps(self.recipe)
             )
        response = self.client.get(
            "/recipes",
            headers= self.headers
            )
        self.assertIn(
            "1.Obtain eggs",
            str(response.data)
            )
        assert response.status=="200 OK"
    