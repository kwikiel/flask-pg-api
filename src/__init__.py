import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from wtforms import Form, TextField
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, flash, jsonify, make_response
import datetime
import jwt

# local
from src.models import *

# Initialize application
app = Flask(__name__, static_folder='templates')
# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'src.config.DevelopmentConfig'
)
app.config.from_object(app_settings)
# Initialize Bcrypt
bcrypt = Bcrypt(app)
# Initialize Flask Sql Alchemy
db = SQLAlchemy(app)

class Base(db.Model):
    __abstract__ = True
    
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class User(Base):
    """
    Table schema
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def save(self):
        """
        Persist the user in the database
        :param user:
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_by_id(user_id):
        """
        Filter a user by Id.
        :param user_id:
        :return: User or None
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        """
        Check a user by their email address
                param: email
                returns: user
        """
        return User.query.filter_by(email=email).first()


# define form scheme
class AuthForm(Form):
    email = TextField('Email:')
    password = TextField('Password:')


@app.route("/", methods=['GET', 'POST'])
def hello():
    """
    Return form if simple browser request and save user in POST request case.
            returns 
            get  -> form template 
            post -> user_id
    """
    form = AuthForm(request.form)
    print(request.form)
    if not form:
        print('well shit')
        print("email: ", request.form['email'],
              "pass: ", request.form['password'])

        if request.method == 'POST':
            user_id = User.save(form)
            return make_response(jsonify({
                "user_id": user_id,
            })), 200

    return render_template('index.html', form=form)


@app.route("/<user_id>", methods=['GET', 'POST'])
def get_user(user_id):
    """
    Get user from DB by id
        param: user_id
        returns user
    """
    user = User.get_by_id(user_id)
    return make_response(jsonify({
        user
    }))


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404
