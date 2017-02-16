from pymongo import MongoClient
from run import app


class Database():
    '''
    DB handler
    open connection
    transmit queries
    close connection
    '''

    def __init__(self):
        mc = MongoClient(app.MONGO_URI)
        self.connection = mc.get_default_database()


    def hello(self):
        return 'hello!'
