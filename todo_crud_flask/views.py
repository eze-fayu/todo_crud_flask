from todo_crud_flask import app

from flask import session
from flask import escape
from flask import send_from_directory
from flask import url_for
from flask import render_template
from flask import request
from flask import abort, redirect, url_for

import service as service

import os


app = Flask(__name__)

# app.config['API_URL'] = os.environ.get('API_URL', 'http://localhost:5000/api/')


@app.route('/')
def index():  # API_URL=app.config['API_URL']
    # url_for('static', filename='css/style.css')
    url_for('static', filename='img/**/*.jpg')
    value = service.get_value()
    return render_template('home.html', value=value)


@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/')
def index():
    return 'Hello World!'