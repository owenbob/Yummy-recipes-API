
import json
from tests.baseTest import BaseTestCase

class Authorization(BaseTestCase):
    
    #-----------------------REGISTER ENDPOINT--------------------------------
    def test_get_at_register_endpoint(self):
        #Testing the register end point
        #If the method is an GET Method Should not be allowed
        
        result=self.client.get("/register")
        assert result.status =="405 METHOD NOT ALLOWED"

    def test_put_at_register_endpoint(self):
        #Testing the register end point
        #If the method is an PUT Method Should not be allowed
        result=self.client.put("/register")
        assert result.status =="405 METHOD NOT ALLOWED"

    def test_delete_at_register_endpoint(self):
        #Testing the register end point
        #If the method is an DELETE Method Should not be allowed
        result=self.client.delete("/register")
        assert result.status =="405 METHOD NOT ALLOWED"
        
    def test_post_at_register_endpoint(self):
        #Testing the register end point
        #If the method is a POST Method Should  be allowed and receive a positive status code
        response = self.client.post("/register")
        assert response.status=="400 BAD REQUEST"

    def test_post_at_register_user(self):
        #Testing the register end point
        #If the method is a POST Method Should  be allowed and receive a positive status code
        #If Data posted through this method,it should allow and have a positce response
        self.user={"username":"Jonas","email":"jonas123@gmail.com","password":"*****"}
        response = self.client.post("/register",data=json.dumps(self.user),headers={"Content-Type":"application/json"})
        assert response.status=="200 OK"

    def test_post_register_endpoint_with_poor_spelling(self):
        #Testing the register end point if method is get but endpoint spelt poorly
        self.user={"username":"Jonas","email":"jonas123@gmail.com","password":"*****"}
        response = self.client.post("/registar",data=json.dumps(self.user),headers={"Content-Type":"application/json"})
        assert response.status=="404 NOT FOUND"

    #-----------------------LOGIN ENDPOINT--------------------------------


    def test_post_at_login_endpoint(self):
        #Testing the login end point
        #If the method is a POST Method Should  be not be allowed 
        response = self.client.post("/login")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_put_at_login_endpoint(self):
        #Testing the login end point
        #If the method is a PUT, Method Should  be not be  allowed
        response = self.client.put("/login")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_delete_at_login_endpoint(self):
        #Testing the login end point
        #If the method is a delete, Method Should  be  not be allowed 
        response = self.client.delete("/login")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_get_at_login_endpoint(self):
        #Testing the login end point
        #If the method is a GET Method Should  be allowed and receive a positive status code
        response = self.client.get("/login")
        assert response.status=="200 OK"


    def test_get_at_login_endpoint_with_poor_spelling(self):
        #Testing the login end point
        #If the method is a GET Method Should  be allowed and receive a positive status code
        response = self.client.get("/Login")
        assert response.status=="404 NOT FOUND"

       
   
        
    
    #----------------------- CREATE_RECIPE ENDPOINT--------------------------------

    def test_post_at_create_recipe_endpoint(self):      
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_recipe")
        assert response.status=="401 UNAUTHORIZED"

    def test_post_at_create_recipe_endpoint_with_poor_spelling(self):      
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create-recipe")
        assert response.status=="404 NOT FOUND"

   
    def test_get_at_create_endpoint_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.get("/create_recipe")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    def test_put_at_create_recipe_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/create_recipe")
        assert response.status=="405 METHOD NOT ALLOWED"


    def test_delete_at_create_recipe_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/create_recipe")
        assert response.status=="405 METHOD NOT ALLOWED"

    #-----------------------RECIPES ENDPOINT--------------------------------

    def test_post_at_recipes_endpoint(self):      
        #Testing the create_receipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/recipes")
        assert response.status=="405 METHOD NOT ALLOWED"

   
    def test_get_at_recipes_endpoint_(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/recipes")
        assert response.status=="401 UNAUTHORIZED"

    def test_get_at_recipes_endpoint_with_poor_spelling(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/Recipes")
        assert response.status=="404 NOT FOUND"

    
    def test_put_at_recipes_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/recipes")
        assert response.status=="405 METHOD NOT ALLOWED"


    def test_delete_at_recipes_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/recipes")
        assert response.status=="405 METHOD NOT ALLOWED"

    

    #-----------------------RECIPE ENDPOINT--------------------------------
    
    def test_post_at_recipe_endpoint(self):      
        #Testing the create_receipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
   
    def test_get_at_recipe_endpoint_(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/recipe/<recipe_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_get_at_recipe_endpoint_with_poor_spelling(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/Recipe/<recipe_id>")
        assert response.status=="404 NOT FOUND"

    
    def test_put_at_recipe_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    def test_delete_at_recipe_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"
    
    
        #----------------------- EDIT RECIPE ENDPOINT--------------------------------
    
    def test_post_at_edit_recipe_endpoint(self):      
        #Testing the create_receipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/edit_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
   

    
    def test_get_at_edit_recipe_endpoint_(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/edit_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    def test_put_at_edit_recipe_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/edit_recipe/<recipe_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_put_at_edit_recipe_endpoint_with_poor_spelling(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/Edit_recipe/<recipe_id>")
        assert response.status=="404 NOT FOUND"


    def test_delete_at_edit_recipe_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/edit_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"


    
    
        #----------------------- DELETE RECIPE ENDPOINT--------------------------------
    
    def test_post_at_delete_recipe_endpoint(self):      
        #Testing the create_receipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/delete_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    

    
    def test_get_at_delete_recipe_endpoint_(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/delete_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    def test_put_at_delete_recipe_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/delete_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"


    def test_delete_at_delete_recipe_endpoint(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/delete_recipe/<recipe_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_delete_at_delete_recipe_endpoint_with_poor_spelling(self):
        #Testing the create_receipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/delete_Recipe/<recipe_id>")
        assert response.status=="404 NOT FOUND"



    