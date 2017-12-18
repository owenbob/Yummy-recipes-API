import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Categories(BaseTestCase):

#-----------------------CATEGORIES ENDPOINT--------------------------------

    def test_post_at_categories_endpoint(self):      
        #Testing the recipes end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/categories")
        assert response.status=="405 METHOD NOT ALLOWED"

   
    def test_get_at_categories_endpoint_(self):
        #Testing the recipes end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/categories")
        assert response.status=="401 UNAUTHORIZED"

    def test_get_at_categories_endpoint_with_poor_spelling(self):
        #Testing the recipes end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("Categories")
        assert response.status=="404 NOT FOUND"

    
    def test_put_at_categories_endpoint(self):
        #Testing the recipes end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code        
        response = self.client.put("/categories")
        assert response.status=="405 METHOD NOT ALLOWED"


    def test_delete_at_categories_endpoint(self):
        #Testing the recipes end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/categories")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    def test_get_at_categories_endpoint_with_token(self):
        #Testing the recipes endpoint
        #If the method is a  get and has a valid token,then we should receive a positive status code
        response = self.client.post(
            "/create_category",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category)
            )
        response = self.client.get(
            "/categories",
            headers= self.headers
            )
        
        self.assertIn(
            "First meal of the morning",
            str(response.data)
            )
        assert response.status=="200 OK"
       