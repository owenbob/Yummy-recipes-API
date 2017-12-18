import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Edit_category(BaseTestCase):
    #----------------------- EDIT CATEGORY ENDPOINT--------------------------------
    
    def test_post_at_edit_category_endpoint(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/edit_category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"
    
    def test_get_at_edit_category_endpoint_(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/edit_category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_put_at_edit_category_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/edit_category/<category_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_put_at_edit_category_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put(
            "/edit_category/<category_id>",
            headers = self.headers, 
            content_type='application/json'
            )
        assert response.status=="404 NOT FOUND"
    
    def test_put_at_edit_category_endpoint_with_category_id(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post(
            "/create_category",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category)
            )

        response2 = self.client.put(
            "/edit_category/1",
            headers = self.headers, 
            content_type='application/json',
            data=json.dumps(self.category)
            )
        self.assertIn(
            "Category has been edited!",
            str(response2.data)
            )
        assert response2.status=="201 CREATED"

    def test_put_at_edit_category_endpoint_with_category_id_with_invalid_data(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post(
            "/create_category",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category)
            )

        response2 = self.client.put(
            "/edit_category/1",
            headers = self.headers, 
            content_type='application/json',
            data=json.dumps(self.invalid_data)
            )
        self.assertIn(
            "Invalid Data Submitted",
            str(response2.data)
            )
        
    def test_put_at_edit_category_endpoint_with_wrong_id(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post(
            "/create_category",
            headers = self.headers, 
            content_type='application/json', 
            data=json.dumps(self.category)
            )
        response3 = self.client.put(
            "/edit_category/3",
            headers = self.headers, 
            content_type='application/json',
            data=json.dumps(self.category)
            )
        self.assertIn(
            "No Category found!",
            str(response3.data)
            )
         
    def test_put_at_edit_category_endpoint_with_poor_spelling(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/Edit_category/<category_id>")
        assert response.status=="404 NOT FOUND"

    def test_delete_at_edit_category_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/edit_category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"