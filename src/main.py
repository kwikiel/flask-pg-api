import os
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import TextField
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, flash, jsonify, make_response
import datetime
import jwt

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
def hello():
    """
    Return form if simple browser request and save user in POST request case.
            returns 
            get  -> form template 
            post -> user_id
    """
    form = AuthForm(request.form)

    # print("%s\n" % type(request.headers['User-Agent']), request.headers['User-Agent'])

    if request.method == 'POST':
        print("email: {} {} pass: {}"
              .format(type(request.form['email']), request.form['email'], request.form['password']))

        user = User(form.email.data, form.password.data)
        user_id = user.save()

        return make_response(jsonify({
            "user_id": user_id,
        })), 200

    return render_template('index.html', form=form)


@app.route("/user/<user_id>", methods=['GET', 'POST'])
def get_user(user_id):
    """
    Get user from DB by id
        param: user_id
        returns user
    """
    print(f"even enter function {user_id}")
    user = User.get_by_id(user_id)
    return make_response(jsonify({
        user
    }))


@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404
