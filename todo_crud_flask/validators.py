# -*- coding: utf8 -*-
from sesh import Sesh


class Validators():
  
    def __init__(self):
        self.name = 'validators'


    def fieldname_as_text(self, fieldname):
        fieldname = fieldname.replace("_", " ")
        fieldname = fieldname.title()
        return fieldname

    def has_presence(self, value):
        try:
            if value:
                # isset
                return True
            else:
                return False
        except NameError:
            # not set
            return False


    def validate_presences(self, form, required_fields):
        sesh = Sesh()
        for field in required_fields:
            value = form[field].strip()
            if not self.has_presence(value):
                sesh.add_error(self.fieldname_as_text(field) + " can't be empty")


    def has_max_length(self, value, max):
        return len(value) <= max


    def validate_max_lengths(self, form, fields_with_max_lengths):
        sesh = Sesh()
        for pair in fields_with_max_lengths:
            for field, max_length in pair.iteritems():
                value = form[field].strip()
                if not self.has_max_length(value, max_length):
                    sesh.add_error("Field input is too long: " + self.fieldname_as_text(field))


    def validate_password_repeated(self, password, repeat):
        sesh = Sesh()
        if password != repeat:
            sesh.add_error("Passwords must match.")

    def validate_unique_username(self, unique_username):
        sesh = Sesh()
        if unique_username:
            sesh.add_error("That username is already taken.")





