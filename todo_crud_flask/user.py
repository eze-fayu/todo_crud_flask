from database import Database
from sesh import Sesh
from flask import escape


def insert_user(form):
    db = Database()
    sesh = Sesh()

    try:
        user = {
          'username': escape(form['username'])
        }
        db.connection['users'].insert_one(user)
        return True

    except Exception, e:
        return str(e)

    # sesh.set_username(user['username'])
    # print sesh.get_username() 



def find_all_users():
    db = Database()
    sesh = Sesh()

    try:
        users = db.connection['users'].find()
        return users

    except Exception, e:
        return str(e)




def update_user(form):
    db = Database()
    sesh = Sesh()
    try:
        db.Employees.update_one(
            {
                "id": criteria
            },
            { 
                "$set": {
                    "email": escape(form['email'])
                }
            }
        )
        return True

    except Exception, e:
        return str(e)




def delete_user(form):
    db = Database()
    sesh = Sesh()

    try:
        user = {
            'id': escape(form['user_id'])
        }
        db.connection['users'].delete_many(user)
        return True

    except Exception, e:
        return str(e)
