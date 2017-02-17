from database import Database
from flask import escape
import datetime

class User():

    def __init__(self):
        self.name = 'User'


    def attempt_login(self, hashing, username, password):
        user = self.find_by_username(username)
        if user:
            if self.password_check(hashing, password, user['hashed_password']):
                return user
            else:
                return False
        else:
            return False


    def password_check(self, hashing, password, hashed_password):
        return hashing.check_value(hashed_password, password, salt='abcd')

    def generate_salt(self):
        return 'abcd'

    def encrypt_password(self, hashing, password):
        return hashing.hash_value(password, salt=self.generate_salt())


    def insert_user(self, hashing, form):
        db = Database()

        username =  escape(form['username'])
        hashed_password = self.encrypt_password(hashing, form['password'])

        try:
            created_at = datetime.datetime.utcnow()
            print created_at
            user = {
              'username': username,
              'hashed_password': hashed_password,
              'created_at': created_at,
              'updated_at': created_at
            }
            db.connection['users'].insert_one(user)
            return True

        except Exception, e:
            return str(e)


    def find_all_users(self):
        db = Database()
        try:
            users = db.connection['users'].find()
            return users

        except Exception, e:
            return str(e)

    def find_by_username(self, username=""):
        db = Database()
        try:
            user = db.connection['users'].find_one(
               { "username": username }
            )
            return user

        except Exception, e:
            return str(e)

    def find_by_id(self, _id=None):
        db = Database()
        try:
            user = db.connection['users'].find_one(
               { "_id": _id }
            )
            return user

        except Exception, e:
            return str(e)


    def update_user(self, form, _id):
        db = Database()
        try:
            res = db.connection['users'].update(
                {'_id': _id},
                { '$set': 
                    { 
                        "email": escape(form['email']),
                        "updated_at": datetime.datetime.utcnow() 
                    } 
                }
            )
            return res['nModified']

        except Exception, e:
            return str(e)



    def delete_user(self, _id):
        db = Database()

        try:
            res = db.connection['users'].delete_one({ '_id': _id })
            return res['nModified']

        except Exception, e:
            return str(e)




