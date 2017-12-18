import json
from tests.baseTest import BaseTestCase

from API.models import User,Category,Recipe
from API import  app
from API.models import db


class Home(BaseTestCase):
       #----------------------- HOME ENDPOINT--------------------------------


    def test_post_at_home_endpoint(self):      
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/home")
        assert response.status=="405 METHOD NOT ALLOWED"

 
    def test_put_at_home_endpoint(self):
        #If the method is a put , Method Should  be not  allowed 
        response = self.client.put("/home")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_delete_at_home_endpoint(self):
        #If the method is delete , Method Should  be not allowed
        response = self.client.delete("/home")
        assert response.status=="405 METHOD NOT ALLOWED"
    
    def test_get_at_home_endpoint(self):
        #If the method is a get , Method Should  be allowed and receive a positive status code 
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
        response = self.client.response = self.client.patch(
            "/set_public_recipe/1",
            headers=self.headers,
            content_type='application/son',
            data=json.dumps(self.recipe)
            )
        response1 = self.client.response = self.client.get("/home")
        self.assertIn("1.Obtain eggs",str(response1.data))
        assert response1.status=="200 OK"
    
    def test_get_at_home_endpoint_(self):
        #If the method is a get , Method Should not be found
        response = self.client.get("/Home")
        assert response.status=="404 NOT FOUND"
    