from pymongo import MongoClient
from config import MONGO_URI

class Database():
    '''
    DB handler
    open connection
    transmit queries
    close connection
    '''

    def __init__(self):
        print 'howdy howdy'
        mc = MongoClient(MONGO_URI)
        self.connection = mc.get_default_database()


    def hello(self):
        return 'hello!'
