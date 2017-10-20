from API.app import app,db
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand



#----------------------------------------------MIGRATIONS------------------------------------------------------------

manager= Manager(app)

migrate = Migrate(app,db)


manager.add_command("db",MigrateCommand)


if __name__ == "main":
    manager.run()

