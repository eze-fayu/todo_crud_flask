# -*- coding: utf8 -*-
# from database import Database
# from flask import escape
# import datetime

class Awards():
    '''
    user class
    password/authentication functions
    DB CRUD handlers
    '''

    def __init__(self):
        self.name = 'Awards'

    def get_award_level(self, score):
        if score >= 100:
            return ('Gold')
        if score >= 50:
            return ('Silver')
        if score >= 25:
            return ('Bronze')
        if score >= 10:
            return ('Tin')
        if score >= 5:
            return ('Stone')
        if score < 5:
            return ('Sand')
