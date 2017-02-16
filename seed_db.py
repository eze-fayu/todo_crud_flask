import json
from pymongo import MongoClient
# from settings import MONGO_URI

MONGO_URI = 'mongodb://localhost:27017/'
### REWRITE THIS?

USERS = 'users'

users = json.load(open('data/users.json'))

mc = MongoClient(MONGO_URI+USERS)
db = mc.get_default_database()

db[USERS].drop()
db[USERS].insert_many(users)

print('Seeded the database with %d users'%db.users.count())


NOTES = 'notes'

notes = json.load(open('data/notes.json'))

mc = MongoClient(MONGO_URI+NOTES)
db = mc.get_default_database()

db[NOTES].drop()
db[NOTES].insert_many(notes)

print('Seeded the database with %d notes'%db.notes.count())