from database import Database
from sesh import Sesh
from flask import escape


def insert_user(form):
    db = Database()
    sesh = Sesh()

    user = {
      'username': escape(form['username'])
    }
    db.connection['users'].insert_many([user])

    sesh.set_username(user['username'])
    
    print sesh.get_username() 


