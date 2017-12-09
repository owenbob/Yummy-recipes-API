
import json
from API.models import User,Category,Recipe
from API import  app
from tests.baseTest import BaseTestCase
from API.models import db


class Authorization(BaseTestCase):

    
    #-----------------------REGISTER ENDPOINT--------------------------------
    def test_get_at_register_endpoint(self):
        #Testing the register end point
        #If the method is an GET Method Should not be allowed
        
        result=self.client.get("/register")
        assert result.status =="405 METHOD NOT ALLOWED" #Change to 400
    
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

    def test_post_with_user_info_at_register_user(self):
        #Testing the register end point
        #If the method is a POST Method Should  be allowed and receive a positive status code
        #If Data posted through this method,it should allow and have a positve response
        #Should also give New user  has been created! message
        self.user={"username":"Jonas","email":"jonas123@gmail.com","password":"*****"}
        response = self.client.post("/register",data=json.dumps(self.user),headers={"Content-Type":"application/json"})
        self.assertIn("New user  has been created!",str(response.data))
        assert response.status=="201 CREATED"
    
    
    def test_post_with_invalid_data_at_register_user(self):
        #Testing the register end point
        #If the method is a POST Method Should  be allowed and receive a positive status code
        #If Data posted through this method,it should allow and have a positce response
        response = self.client.post("/register",data=json.dumps(self.invalid_data),headers={"Content-Type":"application/json"})
        self.assertIn("Invalid Data Submitted",str(response.data))
        assert response.status=="400 BAD REQUEST"


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
        assert response.status=="400 BAD REQUEST"

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
        assert response.status=="400 BAD REQUEST"


    def test_get_at_login_endpoint_with_poor_spelling(self):
        #Testing the login end point
        #If the method is a GET Method Should  be allowed and receive a positive status code
        response = self.client.get("/Login")
        assert response.status=="404 NOT FOUND"
    
    def test_get_at_login_endpoint_with_user_details_who_is_not_registered(self):  
        #Testing the login end point with user credential

        response = self.client.get("/login",data=json.dumps(self.user),headers = self.headers)
        self.assertIn("1.Could not verify",str(response.data))
        assert response.status=="400 BAD REQUEST"




    
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
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))
        self.assertIn("Category created!",str(response.data))
        assert response.status=="201 CREATED"


    def test_post_at_create_category_endpoint_with_invalid_data(self):
         #Testing the create_category end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code but on submiting invalid data
        #Invalid data message should be received
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.invalid_data))
        self.assertIn("Invalid Data Submitted",str(response.data))
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
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))
        response = self.client.get("/categories",headers= self.headers)
        
        self.assertIn("First meal of the morning",str(response.data))
        assert response.status=="200 OK"
       

    
    
    #-----------------------CATEGORY ENDPOINT--------------------------------
    
    def test_post_at_category_endpoint(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
   
    def test_get_at_category_endpoint_(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/category/<category_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_get_at_category_endpoint_with_poor_spelling(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/Category/<category_id>")
        assert response.status=="404 NOT FOUND"

    
    def test_put_at_category_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    def test_delete_at_category_endpoint(self):
        #Testing the recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/category/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    def test_get_at_category_endpoint_with_authorisation(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status
        response = self.client.get("/category/<category_id>",headers = self.headers, content_type='application/json')
        self.assertIn("No Category found!",str(response.data))
        assert response.status=="404 NOT FOUND"
    
        
    def test_get_at_category_endpoint_with_authorisation_and_wrong_category_id(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status but a message that recipe is NOT found
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))
        
        response = self.client.get("/category/3",headers = self.headers, content_type='application/json')
        self.assertIn("No Category found!",str(response.data))
        assert response.status=="404 NOT FOUND"


    
    def test_get_at_category_endpoint_with_authorisation_and_the_category_id(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))
        
        response = self.client.get("/category/1",headers = self.headers, content_type='application/json')
        self.assertIn("First meal of the morning",str(response.data))
        assert response.status=="200 OK"

    

        
       
 
    
    
    
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
        response = self.client.put("/edit_category/<category_id>",headers = self.headers, content_type='application/json')
        assert response.status=="404 NOT FOUND"
    
    def test_put_at_edit_category_endpoint_with_category_id(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response2 = self.client.put("/edit_category/1",headers = self.headers, content_type='application/json',data=json.dumps(self.category))
        self.assertIn("Category has been edited!",str(response2.data))
        assert response.status=="201 CREATED"




    def test_put_at_edit_category_endpoint_with_category_id_with_invalid_data(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response2 = self.client.put("/edit_category/1",headers = self.headers, content_type='application/json',data=json.dumps(self.invalid_data))
        self.assertIn("Invalid Data Submitted",str(response2.data))
        

    def test_put_at_edit_category_endpoint_with_wrong_id(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response3 = self.client.put("/edit_category/3",headers = self.headers, content_type='application/json',data=json.dumps(self.category))
        self.assertIn("No Category found!",str(response3.data))
        
    
    
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
        response = self.client.delete("/delete_category/<category_id>",headers = self.headers,content_type='application/json')
        

    def test_delete_at_category_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response2 = self.client.delete("/delete_category/1",headers = self.headers,content_type='application/json')
        self.assertIn("Category deleted!",str(response2.data))
        
    
    def test_delete_at_category_with_wrong_id_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response2 = self.client.delete("/delete_category/2",headers = self.headers,content_type='application/json')
        self.assertIn("No Category found!",str(response2.data))
        
    
    def test_delete_at_delete_category_endpoint_with_poor_spelling(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/delete_Category/<category_id>")
        assert response.status=="404 NOT FOUND"
    
   
    
       
  
      
    
    #----------------------- CREATE_RECIPE ENDPOINT--------------------------------

    def test_post_at_create_recipe_endpoint(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_recipe/<category_id>")
        assert response.status=="401 UNAUTHORIZED"
    
    
    def test_post_at_create_recipe_endpoint(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response = self.client.post("/create_recipe/1",headers = self.headers, content_type='application/json', data=json.dumps(self.recipe))
        self.assertIn("Recipe created!",str(response.data))
        assert response.status=="201 CREATED"


    def test_post_at_create_recipe_endpoint_with_invalid_data(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response = self.client.post("/create_recipe/1",headers = self.headers, content_type='application/json', data=json.dumps(self.invalid_data))
        self.assertIn("Invalid Data Submitted",str(response.data))
        assert response.status=="400 BAD REQUEST"
    
    
    
    def test_post_at_create_recipe_endpoint_with_poor_spelling(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create-recipe/<category_id>")
        assert response.status=="404 NOT FOUND"

   
    def test_get_at_create_endpoint_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.get("/create_recipe/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    def test_put_at_create_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/create_recipe/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    def test_delete_at_create_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/create_recipe/<category_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    
    
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
        response = self.client.get("/recipe/<recipe_id>",headers = self.headers, content_type='application/json')
        assert response.status=="404 NOT FOUND"
    
    
    def test_get_at_recipe_endpoint_with_authorisation_and_wrong_recipe_id(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status but a message that recipe is NOT found
        response = self.client.post("/create_recipe",headers = self.headers, content_type='application/json', data=json.dumps(self.recipe))
        
        response = self.client.get("/recipe/4",headers = self.headers, content_type='application/json')
        self.assertIn("No Recipe found!",str(response.data))
        assert response.status=="404 NOT FOUND"
    
    
    def test_get_at_recipe_endpoint_with_authorisation_and_the_recipe_id(self):
        #Testing the recipe end point
        #If the method is a get ,and with proper with authorisation then should have a positive status
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response = self.client.post("/create_recipe/1",headers = self.headers, content_type='application/json', data=json.dumps(self.recipe))
        response = self.client.get("/recipes",headers= self.headers)
        
        self.assertIn("1.Obtain eggs",str(response.data))
        assert response.status=="200 OK"
    
    
        
       
 
    
    
    
        #----------------------- EDIT RECIPE ENDPOINT--------------------------------
    
    def test_post_at_edit_recipe_endpoint(self):      
        #Testing the create_recipe end point
        #If the method is a Post , Method Should not be allowed 
        response = self.client.post("/edit_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

        
    def test_get_at_edit_recipe_endpoint_(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed but receive unauthorized status
        response = self.client.get("/edit_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

    
    def test_put_at_edit_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/edit_recipe/<recipe_id>")
        assert response.status=="401 UNAUTHORIZED"

    def test_put_at_edit_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response = self.client.post("/create_recipe/1",headers = self.headers, content_type='application/json', data=json.dumps(self.recipe))
        response2 = self.client.put("/edit_recipe/1",headers = self.headers, content_type='application/json',data=json.dumps(self.recipe))
        self.assertIn("Recipe has been edited!",str(response2.data))
        assert response.status=="201 CREATED"


    def test_put_at_edit_recipe_endpoint_with_invalid_data(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response = self.client.post("/create_recipe/1",headers = self.headers, content_type='application/json', data=json.dumps(self.recipe))
        response2 = self.client.put("/edit_recipe/1",headers = self.headers, content_type='application/json',data=json.dumps(self.invalid_data))
        self.assertIn("Invalid Data Submitted",str(response2.data))
        

    
    def test_put_at_edit_recipe_endpoint_with_poor_spelling(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.put("/Edit_recipe/<recipe_id>")
        assert response.status=="404 NOT FOUND"


    def test_delete_at_edit_recipe_endpoint(self):
        #Testing the create_recipe end point
        #If the method is a Post , Method Should  be allowed and receive a positive status code
        response = self.client.delete("/edit_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"


    
   
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
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))
        response = self.client.post("/create_recipe/1",headers = self.headers, content_type='application/json', data=json.dumps(self.recipe))

        response = self.client.delete("/delete_recipe/1",headers = self.headers,content_type='application/json',data=json.dumps(self.recipe))
        assert response.status=="200 OK"

    def test_delete_at_delete_recipe_endpoint_with_poor_spelling(self):
        #If the method is a delete , Method Should not be allowed 
        response = self.client.delete("/delete_Recipe/<recipe_id>")
        assert response.status=="404 NOT FOUND"


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
        response = self.client.post("/create_category",headers = self.headers, content_type='application/json', data=json.dumps(self.category))

        response = self.client.post("/create_recipe/1",headers = self.headers, content_type='application/json', data=json.dumps(self.recipe))
        self.assertIn("Recipe created!",str(response.data))
        response1 = self.client.response = self.client.patch("/set_public_recipe/1",headers=self.headers,content_type='application/son',data=json.dumps(self.recipe))
        self.assertIn("Recipe is now Public",str(response1.data))
        # import pdb ; pdb.set_trace()
        assert response1.status=="201 CREATED"
    
    def test_get_at_set_public_recipe_endpoint_(self):
        #If the method is a get , Method Should not be allowed
        response = self.client.get("/set_public_recipe/<recipe_id>")
        assert response.status=="405 METHOD NOT ALLOWED"

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
        self.assertIn("Recipe created!",str(response.data))
        response = self.client.response = self.client.patch(
            "/set_public_recipe/1",
            headers=self.headers,
            content_type='application/son',
            data=json.dumps(self.recipe)
            )
        self.assertIn("Recipe is now Public",str(response.data))
        response1 = self.client.response = self.client.get("/home")
        self.assertIn("1.Obtain eggs",str(response1.data))
        assert response1.status=="200 OK"
    
    def test_get_at_home_endpoint_(self):
        #If the method is a get , Method Should not be found
        response = self.client.get("/Home")
        assert response.status=="404 NOT FOUND"

    