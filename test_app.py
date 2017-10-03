#testing App endpoints

from app import app
def test_register_endpoint():
    #Testing the register end point
    #If the method is an GET Method Should not be allowed
    client=app.test_client()
    result=client.get("/register")
    assert result.status =="405 METHOD NOT ALLOWED"

def test_post_register_endpoint():
    #Testing the register end point
    #If the method is an GET Method Should not be allowed
    client=app.test_client()
    result=client.post("/register")
    assert result.status =="200 OK"