import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Delete_recipe(BaseTestCase):
        #----------------------- DELETE RECIPE ENDPOINT--------------------------------
    
    def test_post_at_delete_recipe_endpoint(self): 
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/delete_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_get_at_delete_recipe_endpoint_(self):
        #If the method is a get , Method Should not be allowed 
        response = self.client.get("/delete_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_put_at_delete_recipe_endpoint(self):
        #If the method is a put , Method Should not be allowed 
        response = self.client.put("/delete_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_delete_at_delete_recipe_endpoint(self):
        #If the method is a delete , Method Should  be allowed and receive a unauthorised status code
        response = self.client.delete("/delete_recipe/<recipe_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_delete_at_delete_recipe_endpoint(self):
        #If the method is a delete , Method Should  be allowed and receive a positive status code
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

        response = self.client.delete(
            "/delete_recipe/1",
            headers = self.headers,
            content_type='application/json',
            data=json.dumps(self.recipe)
            )
        assert response.status=="200 OK"

    def test_delete_at_delete_recipe_endpoint_with_poor_spelling(self):
        #If the method is a delete , Method Should not be allowed 
        response = self.client.delete("/delete_Recipe/<recipe_id>")
        assert response.status=="404 NOT FOUND"
