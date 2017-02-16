from flask import Flask
from flask import send_from_directory
from flask import url_for
from flask import render_template
from flask import request
from flask import abort, redirect, url_for

import os


app = Flask(__name__)

app.config['API_URL'] = os.environ.get('API_URL', 'http://localhost:5000/api/')


@app.route('/')
def index(API_URL=app.config['API_URL']):
    url_for('static', filename='css/style.css')
    url_for('static', filename='img/**/*.jpg')
    return render_template('index.html', API_URL=API_URL)


@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<int:user_id>')
def show_user(user_id):
    # show the user profile for that user
    return 'User id %d' % user_id

# @app.route('/note/<int:note_id>')
# def show_note(note_id):
#     # show the post with the given id, the id is an integer
#     return 'Note id %d' % note_id

@app.route('/note/')
@app.route('/note/<int:note_id>')
def render(note_id=None):
    return render_template('note.html', note_id=note_id)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)






@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(port=8000,debug=True)

