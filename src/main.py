import os
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import TextField
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, flash, jsonify, make_response
import datetime
import json
import jwt

from src.serialization import AlchemyEncoder

# local

# Initialize application
app = Flask(__name__, static_folder='templates')
# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'src.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

db = SQLAlchemy(app)

from src.models import User

# define form scheme

class AuthForm(FlaskForm):
    email = TextField('Email:')
    password = TextField('Password:')


@app.route("/", methods=['GET', 'POST'])
def index():
    """
    Return form if simple browser request and save user in POST request case.
            returns 
            get  -> form template 
            post -> user_id
    """
    form = AuthForm(request.form)

    if request.method == 'POST':
        user = User(form.email.data, form.password.data)
        user_id = user.save()
        
        if not user_id:
            return "Failure: could not save user"

        return make_response(jsonify({
            "user_id": user_id,
        })), 200

    return render_template('index.html', form=form)


@app.route("/user/<user_id>", methods=['GET', 'POST'])
def user_interact(user_id):
    """
    Get user from DB by id
        param: user_id
        returns user
    """

    # update user
    if request.method == 'POST':
        form = AuthForm(request.form)
        User.update(user_id, {'email': form.email.data,
                              'password': form.password.data})
        return f"Successfully updated user {user_id}\n"
    
    # get user
    user = User.get_by_id(user_id)
    return make_response(json.dumps(user, cls=AlchemyEncoder))


@app.errorhandler(404)
def page_not_found(e):
    return "Not found", 404
