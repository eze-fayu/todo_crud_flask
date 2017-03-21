# -*- coding: utf8 -*-
from flask import flash, session, url_for, redirect
from bson.objectid import ObjectId


class Sesh():
    '''
    wrapper class for flask session
    tracks logged in/logged out
    tracks username and user_id
    tracks messages between routes
    tracks errors
    '''

    def __init__(self):
        self.name = 'sesh'


    def confirm_logged_in(self):
        if not self.get_logged_in():
            flash("You must be logged in to do that.")
            return False
        else:
            return True
            redirect(url_for('login_route'))

    def confirm_not_logged_in(self):
        if self.get_logged_in():
            flash("You must be logged out to do that.")
            return False
        else:
            return True

    def get_logged_in(self):
        return session.get('logged_in')

    def set_logged_in(self, input):
        session['logged_in'] = input
        return True

    def unset_logged_in(self,):
        session.pop('logged_in', None)
        return True

    def get_username(self):
        return session.get('username')

    def set_username(self, input):
        session['username'] = input
        return True

    def unset_username(self):
        session.pop('username', None)
        return True

    def get_user_id(self):
        return session.get('user_id')

    def get_user_id_as_string(self):
        return str(session.get('user_id')) if session.get('user_id') else ""

    def set_user_id(self, input):
        session['user_id'] = input
        return True

    def set_user_id_as_string(self, input):
        session['user_id'] = ObjectId(input)


    def unset_user_id(self):
        session.pop('user_id', None)
        return True

