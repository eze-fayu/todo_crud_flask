# -*- coding: utf8 -*-
from todo_crud_flask.database import Database
from flask import escape
import datetime


class Note():
    '''
    note class
    DB CRUD handlers
    '''

    def __init__(self):
        self.name = 'Note'


    def insert_note(self, user_id, title="", note_type="", content=""):
        db = Database()

        title =  escape(title)
        note_type =  escape(note_type)
        content =  escape(content)

        try:
            created_at = datetime.datetime.utcnow()
            note = {
              'user_id': user_id,
              'created_at': created_at,
              'updated_at': created_at,              
              'title': title,
              'type': note_type,
              'content': content
            }
            res = db.connection['notes'].insert_one(note)
            res_user = db.connection['users'].update(
                {'_id': user_id},
                { '$inc': { 'score': 3 } }
            )
            return res.inserted_id

        except Exception as e:
            return str(e)


    def find_all_notes(self):
        db = Database()
        try:
            res = db.connection['notes'].find()
            return res

        except Exception as e:
            return str(e)


    def find_by_id(self, _id=None):
        db = Database()
        try:
            res = db.connection['notes'].find_one( { "_id": _id } )
            return res

        except Exception as e:
            return str(e)

    def find_by_user_id(self, user_id=None):
        db = Database()
        try:
            res = db.connection['notes'].find( { "user_id": user_id } )
            return res

        except Exception as e:
            return str(e)


    def update_note(self, user_id, _id, title="", content="", note_type="" ):
        db = Database()
        try:
            res = db.connection['notes'].update(
                {'_id': _id},
                { '$set': 
                    { 
                        "title": escape(title),
                        "content": escape(content),
                        "type": escape(note_type),
                        "updated_at": datetime.datetime.utcnow()
                    }, 
                }
            )
            res_user = db.connection['users'].update(
                {'_id': user_id},
                { '$inc': { 'score': 1 } }
            )
            return res['nModified']

        except Exception as e:
            return str(e)


    def belongs_to_user(self, _id, user_id):
        db = Database()
        try:
            res = db.connection['notes'].find_one( { "_id": _id, "user_id": user_id } )
            return res
            
        except Exception as e:
            return str(e)



    def delete_note(self, _id, user_id):
        db = Database()
        try:
            res = db.connection['notes'].delete_one({ '_id': _id, 'user_id': user_id })
            res_user = db.connection['users'].update(
                {'_id': user_id},
                { '$inc': { 'score': 1 } }
            )
            return res.deleted_count

        except Exception as e:
            return str(e)

    def delete_all_user_notes(self, user_id):
        db = Database()
        try:
            res = db.connection['notes'].delete_many({ 'user_id': user_id })
            return res.deleted_count

        except Exception as e:
            return str(e)

