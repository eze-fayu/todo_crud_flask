# todo_crud_flask

A todo-list CRUD app built with Flask + MongoDB.

Example: [https://todo-crud-flask.herokuapp.com](https://todo-crud-flask.herokuapp.com)

## App

Create user accounts with a username and password. Passwords are salted and hashed.

Create TODO notes and view them in your user dashboard. Update notes or delete them.

Update your profile with your email address. Delete your account to erase your data, including all your notes.


## Development

Clone the repository and create a virtualenv

```
$ git clone https://github.com/andrewmontes87/todo-crud-flask.git
$ cd todo_crud_flask
$ virtualenv venv
```

Add these two lines to `venv/bin/activate`, using a secret key and your mLab credentials:

```
export SECRET_KEY={'your secret key'}
export MONGO_URI={'mongodb://user:pass@domain.mlab.com:port/user}'
```

Start the virtualenv

`$ source venv/bin/activate`

Install packages

`(venv)$ pip install -r requirements.txt`

Start the app

`(venv)$ python todo_crud_flask/routes.py`

The app will be at `http://localhost:8000`



### Styles

To watch scss files for changes during development:

`sass --watch todo_crud_flask/static/scss/main.scss:todo_crud_flask/static/css/style.css`


## Deploy

Set config variables in Heroku:
- MONGO_URI
- SECRET_KEY

Push to heroku



## TODO

flask-script for command-line options

flask-moment for datetimes

Templating with super()

Use flash() for messages

404 and 500 pages

Validate password + repeat password using EqualTo

Redirect all POSTs

flask-mail

Package instead of module

Blueprints

Tests












