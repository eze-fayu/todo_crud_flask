# -*- coding: utf8 -*-
from pymongo import MongoClient
import os
import dns

class Database():
    '''
    DB handler
    open connection
    '''

    def __init__(self):
        MONGO_URI = os.environ.get('MONGO_URI', 'http://localhost:27017')
        mc = MongoClient(MONGO_URI)
        self.connection = mc.get_default_database()
