import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db

class Create_category(BaseTestCase):

    #----------------------- CREATE_CATEGORY ENDPOINT--------------------------------

    def test_post_at_create_category_endpoint(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_category")
        assert response.status=="401 UNAUTHORIZED"


    def test_post_at_create_category_endpoint_with_category_details(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        #Should receive message Category created
        response = self.client.post(
            "/create_category",headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category)
            )
        self.assertIn(
            "This category  title already exists",
            str(response.data)
            )
        assert response.status=="201 CREATED"

    def test_post_at_create_category_endpoint_with_category_details(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        #Should receive message Category created
        response = self.client.post(
            "/create_category",headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category2)
            )
        self.assertIn(
            "Category created!",
            str(response.data)
            )
        assert response.status=="201 CREATED"

    def test_post_at_create_category_endpoint_with_invalid_data(self):
            #Testing the create_category end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code but on submiting invalid data
        #Invalid data message should be received
        response = self.client.post(
            "/create_category",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.invalid_data)
            )
        self.assertIn(
            "Invalid Data Submitted",
            str(response.data)
            )
        assert response.status=="400 BAD REQUEST"
        


    def test_post_at_create_category_endpoint_with_poor_spelling(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_Category")
        assert response.status=="404 NOT FOUND"


    def test_get_at_create_category_endpoint_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.get("/create_category")
        assert response.status=="405 METHOD NOT ALLOWED"


    def test_put_at_create_category_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/create_category")
        assert response.status=="405 METHOD NOT ALLOWED"


    def test_delete_at_create_category_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/create_category")
        assert response.status=="405 METHOD NOT ALLOWED"