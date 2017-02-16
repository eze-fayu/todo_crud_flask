from flask import Flask, session, escape, \
    send_from_directory, url_for, render_template, \
    request, abort, redirect, url_for

import os

import service as service

app = Flask(__name__)

@app.route('/')
def index():  # API_URL=app.config['API_URL']
    # url_for('static', filename='css/style.css')
    url_for('static', filename='img/**/*.jpg')
    value = service.get_value()
    return render_template('home.html', value=value)


@app.route('/hello')
def hello():
    return 'Hello, World'

