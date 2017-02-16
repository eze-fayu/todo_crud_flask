from flask import Flask, session, escape, \
    send_from_directory, url_for, render_template, \
    request, abort, redirect, url_for

import os

import functions as Functions
import user as User
from sesh import Sesh


app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY', 'development_secret_key')
app.MONGO_URI = os.getenv('MONGO_URI', 'http://localhost:27017')

sesh = Sesh()


def before_route_load():
    url_for('static', filename='img/**/*.jpg')
    return True

@app.route('/')
def home_route():
    before_route_load()
    value = Functions.get_value()
    return render_template('home.html', value=value)



@app.route('/login', methods=['GET', 'POST'])
def login_route():
    before_route_load()
    return render_template('login.html')



@app.route('/logout', methods=['GET', 'POST'])
def logout_route():
    before_route_load()
    return render_template('logout.html')


@app.route('/new_user', methods=['GET', 'POST'])
def new_user_route():
    before_route_load()
    error = None
    if request.method == 'POST':
        sesh.set_username("none")
        print sesh.get_username()
        User.insert_user(form=request.form)
        return redirect(url_for('update_user_route'))
    return render_template('new_user.html', error=error) 






@app.route('/update_user', methods=['GET', 'POST'])
def update_user_route():
    before_route_load()
    return render_template('update_user.html') 



@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user_route():
    before_route_load()
    return render_template('delete_user.html') 



@app.route('/dashboard')
def dashboard_route():
    before_route_load()
    return render_template('dashboard.html') 




@app.route('/hello')
def hello():
    return 'Hello, World'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(port=8000,debug=True)