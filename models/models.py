





#User Model in SQL
class User(db.Model):
    
    __table__ = "Users"

    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(50))
    email = db.Column(db.String(60))
    password = db.Column(db.String(80))


    def __init__(self,username,email, password):
        #initiliazing User class constructor
        self.username=username
        self.email = email
        self.password = password



    def create(self):
        #method to create a new record in the databse
        db.session.add(self)
        db.session.commit()

    def update(self):
        #method to make changes to a record in the datase
        db.session.commit()

    def delete(self):
        #method to delete record in database
        db.session.delete()
        db.session.commit()
    



    

class Recipe(db.Model):
    
    __table__ = "Recipes"

    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(1000))
    id = db.Column(db.Integer)



        def __init__(self,recipe_id,title,user_id):
            #initiliazing User class constructor
        self.recipe_id=recipe_id
        self.title = title
        self.user_id = user_id


    def create(self):
        #method to create new record in the databse
        db.session.add(self)
        db.session.commit()

    def update(self):
        #method to make changes to a record in the datase
        db.session.commit()

    def delete(self):
        #method to delete record  in database
        db.session.delete()
        db.session.commit()