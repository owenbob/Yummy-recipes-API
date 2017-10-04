
import json
from tests.baseTest import BaseTestCase

class Authorization(BaseTestCase):
    def test_get_register_endpoint(self):
        #Testing the register end point
        #If the method is an GET Method Should not be allowed
        
        result=self.client.get("/register")
        assert result.status =="405 METHOD NOT ALLOWED"

    def test_put_register_endpoint(self):
        #Testing the register end point
        #If the method is an PUT Method Should not be allowed
        result=self.client.put("/register")
        assert result.status =="405 METHOD NOT ALLOWED"

    def test_delete_register_endpoint(self):
        #Testing the register end point
        #If the method is an DELETE Method Should not be allowed
        result=self.client.delete("/register")
        assert result.status =="405 METHOD NOT ALLOWED"
        
    def test_post_register_endpoint(self):
        #Testing the register end point
        #If the method is a POST Method Should  be allowed and receive a positive status code
        #user = json.dumps({"username":"Jonas","email":"jonas123@gmail.com","password":"*****"})
        response = self.client.post("/register")
        assert response.status=="400 BAD REQUEST"

    def test_post_register_user(self):
        #Testing the register end point
        #If the method is a POST Method Should  be allowed and receive a positive status code
        self.user={"username":"Jonas","email":"jonas123@gmail.com","password":"*****"}
        response = self.client.post("/register",data=json.dumps(self.user),headers={"Content-Type":"application/json"})
        assert response.status=="200 OK"






        #  response = self.app.post(
        #         "/auth/register",
        #         content_type="application/json",
        #         data=json.dumps({"username": self.fakes.user_name(), "password": self.fakes.password()})
        #         )
        #     self.assertEqual(response.status_code, 201)