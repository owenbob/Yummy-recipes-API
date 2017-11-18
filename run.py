#-----------------------------------------RUNNING APP-----------------------------------------------------
from API.app import app,db



if __name__ == "__main__":
    app.run(debug=True)