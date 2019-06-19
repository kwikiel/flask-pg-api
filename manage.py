from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src import app, db, models
from src.models import User
from psycopg2.errors import UndefinedTable
import os

# Initializing the manager
manager = Manager(app)

# Initialize Flask Migrate
migrate = Migrate(app, db)

# Add the flask migrate
manager.add_command('db', MigrateCommand)

@manager.command
def init():
    try:
        print(User.get_by_id(0))
    except UndefinedTable:
        print("No 'users' table")
    except:
        db.create_all()
        db.session.commit()

        admin = User('admin', 'admin@example.com')
        guest = User('guest', 'guest@example.com')
        db.session.add(admin)
        db.session.add(guest)
        db.session.commit()
        users = User.query.all()
        print (users)
    # Create a user if they do not exist.
    # user = User.query.filter_by(email="example@bucketmail.com").first()
    # if not user:
    #     user = User("example@bucketmail.com", "123456")
    #     user.save()

# Run the manager
if __name__ == '__main__':
    manager.run()
