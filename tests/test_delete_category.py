import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Deletecategory(BaseTestCase):
        #----------------------- DELETE CATEGORY ENDPOINT--------------------------------
    
    def test_post_at_delete_category_endpoint(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/delete_category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
     
    def test_get_at_delete_category_endpoint_(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/delete_category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    def test_put_at_category_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/delete_category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"


    def test_delete_at_category_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/delete_category/<category_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_delete_at_category_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete(
            "/delete_category/<category_id>",
            headers = self.headers,
            content_type='application/json'
            )
        

    def test_delete_at_category_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post(
            "/create_category",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category)
            )

        response2 = self.client.delete(
            "/delete_category/1",
            headers = self.headers,
            content_type='application/json'
            )
        self.assertIn(
            "Category deleted!",
            str(response2.data)
            )
        
    
    def test_delete_at_category_with_wrong_id_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post(
            "/create_category",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category)
            )

        response2 = self.client.delete(
            "/delete_category/2",
            headers = self.headers,
            content_type='application/json'
            )
        self.assertIn(
            "No Category found!",
            str(response2.data)
            )
        
    
    def test_delete_at_delete_category_endpoint_with_poor_spelling(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/delete_Category/<category_id>")
        assert response.status=="404 NOT FOUND"