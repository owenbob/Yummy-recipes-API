
[![Build Status](https://travis-ci.org/owenbob/Yummy-recipes-API.svg?branch=master)](https://travis-ci.org/owenbob/Yummy-recipes-API)
[![Coverage Status](https://coveralls.io/repos/github/owenbob/Yummy-recipes-API/badge.svg)](https://coveralls.io/github/owenbob/Yummy-recipes-API)
[![CircleCI](https://circleci.com/gh/owenbob/Yummy-recipes-API.svg?style=svg)](https://circleci.com/gh/owenbob/Yummy-recipes-API)


# Yummy-recipes-API

##  Its a RESTful API using Flask with Endpoints that:
   * Enable users to register, login and manage their accounts
   * 
    
    | Sample EndPoint      | Public Access |
    | -------------------- |:-------------:| 
    | POST /auth/register  | TRUE          | 
    | POST /auth/login     | TRUE          |  
    

   * Enable users to use the required features.
   * Implement Token Based Authentication for the API such that methods besides login and register are not accessible to unauthenticated users.


## Installation
First clone this repository
```
$ git clone https://github.com/owenbob/https://github.com/owenbob/Yummy-recipes-API
$ cd Yummy-recipes-API
```
Create virtual environment and install it
```
$ virtualenv env
$ source/env/bin/activate
```
Then install all the necessary dependencies
```
pip install -r requirements.txt
```

## Run the application
At the terminal or console type
```
python run.py
```
To run tests  cd into tests directory run this command at the console/terminal
```
pytest name_of_test eg pytest test_app.py

```


##Test
```
To test using  CURL or POSTMAN (a google chrome extention)
```
##Python Version Used
```
Python 3.6
```
## Do share you thoughts and ideas  because together we learn more.  


