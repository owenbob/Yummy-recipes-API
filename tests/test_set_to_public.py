import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Set_to_public(BaseTestCase):
     #----------------------- SET TO PUBLIC ENDPOINT--------------------------------


    def test_post_at_set_public_recipe_endpoint(self):    
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/set_public_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_put_at_delete_public_recipe_endpoint(self):
        #If the method is delete , Method Should  be not allowed
        response = self.client.delete("/set_public_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"
    
    def test_put_at_set_public_recipe_endpoint(self):
        #If the method is a put , Method Should  be allowed and receive a positive status code
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
        self.assertIn(
            "Recipe created!",
            str(response.data)
            )
        response1 = self.client.response = self.client.patch(
            "/set_public_recipe/1",
            headers=self.headers,
            content_type='application/son',
            data=json.dumps(self.recipe)
            )
        self.assertIn(
            "Recipe is now Public",
            str(response1.data)
            )
        assert response1.status=="201 CREATED"
    
    def test_get_at_set_public_recipe_endpoint_(self):
        #If the method is a get , Method Should not be allowed
        response = self.client.get("/set_public_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"