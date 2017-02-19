# -*- coding: utf8 -*-
from flask_wtf import FlaskForm 
from wtforms import StringField, HiddenField, PasswordField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired("Please enter your username")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password")])
  submit = SubmitField("Login")

class LogoutForm(FlaskForm):
  password = HiddenField('logout', default="true", validators=[DataRequired("Something went wrong logging you out")])
  submit = SubmitField("Logout")

class NewUserForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired("Please enter a username"), Length(min=8, message="Usernames must be 8 characters or more."), Length(max=30, message="Usernames must be less than 30 characters.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password"), Length(min=8, message="Passwords must be 8 characters or more."), Length(max=30, message="Passwords must be less than 30 characters.")])
  repeat_password = PasswordField('Repeat Password', validators=[DataRequired("Please re-enter your password"), Length(min=8, message="Passwords must be 8 characters or more."), Length(max=30, message="Passwords must be less than 30 characters.")])
  submit = SubmitField("Create user")

class UpdateUserForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  submit = SubmitField("Save")

class DeleteUserForm(FlaskForm):
  delete = HiddenField('delete', default="true", validators=[DataRequired("Something went wrong deleting your account: no delete tag")])
  submit = SubmitField("Delete")

class GoToEditNoteForm(FlaskForm):
    # this is just to generate a csrf tag
    submit = SubmitField("Edit")

class EditNoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired("Please enter a note title")])
    note_type = SelectField('Note Type', 
                        choices=[('TODO', 'TODO'), ('Reminder', 'Reminder'), ('Misc.', ' Misc.')],
                        default="TODO")
    content = TextAreaField('Note Content', validators=[Length(max=500, message="Note must be less than 500 characters.")])
    note_id = HiddenField('note_id', default="new_id", validators=[DataRequired("Something went wrong saving your note")])
    submit = SubmitField("Save")

class DeleteNoteForm(FlaskForm):
  note_id = HiddenField('note_id', default="new_id", validators=[DataRequired("Something went wrong deleting your note: no note_id tag")])
  submit = SubmitField("Delete")

