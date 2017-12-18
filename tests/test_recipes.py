import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Recipes(BaseTestCase):
    #-----------------------RECIPES ENDPOINT--------------------------------

    def test_post_at_recipes_endpoint(self):      
        #Testing the recipes end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/recipes")
        assert response.status=="405 METHOD NOT ALLOWED"

   
    def test_get_at_recipes_endpoint_(self):
        #Testing the recipes end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/recipes")
        assert response.status=="401 UNAUTHORIZED"

    def test_get_at_recipes_endpoint_with_poor_spelling(self):
        #Testing the recipes end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/Recipes")
        assert response.status=="404 NOT FOUND"

    
    def test_put_at_recipes_endpoint(self):
        #Testing the recipes end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/recipes")
        assert response.status=="405 METHOD NOT ALLOWED"


    def test_delete_at_recipes_endpoint(self):
        #Testing the recipes end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/recipes")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    
    def test_get_at_recipes_endpoint_with_token(self):
        #Testing the reci[es endpoint
        #If the method is a  get and has a valid token,then we should receive a positive status code
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response = self.client.post("/create_recipe/1",headers = self.headers, content_type='application/json', data=json.dumps(self.recipe))
        response = self.client.get("/recipes",headers= self.headers)
        
        self.assertIn("1.Obtain eggs",str(response.data))
        assert response.status=="200 OK"
    
      