# todo_crud_flask

A todo-list CRUD app built with Flask + MongoDB.

Example: [https://todo-crud-flask.herokuapp.com](https://todo-crud-flask.herokuapp.com)

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

`(venv)$ source venv/bin/activate`

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



## Notes

Finished
- project structure
- deployed on heroku
- mongodb connected
- user routes laid out
- database class
- user class
- user.insert_user

TODO
- session class
- user read methods
- login/logout
- user delete methods
- delete_user route
- dashboard route
- user update methods
- update_user route
- notes CRUD
- cleanup


