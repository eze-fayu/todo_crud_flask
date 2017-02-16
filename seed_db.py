import json
from pymongo import MongoClient
from settings import MONGO_URI

mc = MongoClient(MONGO_URI)
db = mc.get_default_database()


users = json.load(open('data/users.json'))

USERS = 'users'

db[USERS].drop()
db[USERS].insert_many(users)

print('Seeded the database with %d users'%db.users.count())


notes = json.load(open('data/notes.json'))

NOTES = 'notes'

db[NOTES].drop()
db[NOTES].insert_many(notes)

print('Seeded the database with %d notes'%db.notes.count())