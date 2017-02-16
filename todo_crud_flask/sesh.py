from flask import session


class Sesh():
    '''
    session handler
    tracks logged in/logged out
    tracks username and user_id
    tracks messages between routes
    '''

    def __init__(self):
        self.name = 'sesh'


    def get_logged_in(self):
        return session['logged_in']

    def set_logged_in(self, input):
        session['logged_in'] = input
        return True

    def get_username(self):
        return session['username']

    def set_username(self, input):
        session['username'] = input
        return True

    def get_user_id(self):
        return session['user_id']

    def set_user_id(self, input):
        session['user_id'] = input
        return True

    def get_messages(self):
        return session['messages']

    def add_messages(self, input):
        session['messages'].append(input)
        return True

    def clear_messages(self):
        session['messages'] = []
        return True

