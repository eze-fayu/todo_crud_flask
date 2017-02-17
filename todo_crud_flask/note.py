from database import Database
from flask import escape
import datetime


class Note():

    def __init__(self):
        self.name = 'Note'



    def insert_note(self, form, user_id):
        db = Database()

        title =  escape(form.get('title', ""))
        content =  escape(form.get('content', ""))
        this_type =  escape(form.get('type', ""))

        try:
            created_at = datetime.datetime.utcnow()
            note = {
              'title': title,
              'type': this_type,
              'content': content,
              'user_id': user_id,
              'created_at': created_at,
              'updated_at': created_at,
            }
            res = db.connection['notes'].insert_one(note)
            return res.inserted_id

        except Exception, e:
            return str(e)


    def find_all_notes(self):
        db = Database()
        try:
            res = db.connection['notes'].find()
            return res

        except Exception, e:
            return str(e)


    def find_by_id(self, _id=None):
        db = Database()
        try:
            res = db.connection['notes'].find_one(
               { "_id": _id }
            )
            return res

        except Exception, e:
            return str(e)

    def find_by_user_id(self, user_id=None):
        db = Database()
        try:
            res = db.connection['notes'].find(
               { "user_id": user_id }
            )
            return res

        except Exception, e:
            return str(e)


    def update_note(self, form, _id):
        db = Database()
        try:
            res = db.connection['notes'].update(
                {'_id': _id},
                { '$set': 
                    { 
                        "title": escape(form['title']),
                        "content": escape(form['content']),
                        "type": escape(form['type']),
                        "updated_at": datetime.datetime.utcnow()
                    }, 
                }
            )
            return res['nModified']

        except Exception, e:
            return str(e)



    def delete_note(self, _id, user_id):
        db = Database()
        try:
            res = db.connection['notes'].delete_one({ '_id': _id, 'user_id': user_id })
            return res.deleted_count

        except Exception, e:
            return str(e)

    def delete_all_user_notes(self, user_id):
        db = Database()
        try:
            res = db.connection['notes'].delete_many({ 'user_id': user_id })
            return res.deleted_count

        except Exception, e:
            return str(e)

