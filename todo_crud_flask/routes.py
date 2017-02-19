# -*- coding: utf8 -*-

import os
from bson.objectid import ObjectId

from flask import Flask, session, escape, \
    send_from_directory, url_for, render_template, \
    request, abort, redirect, Markup
from flask_hashing import Hashing
from flask_wtf.csrf import CSRFProtect

from user import User
from note import Note
from sesh import Sesh
from validators import Validators
from forms import LoginForm, \
                  LogoutForm, \
                  NewUserForm, \
                  UpdateUserForm, \
                  DeleteUserForm, \
                  EditNoteForm, \
                  GoToEditNoteForm, \
                  DeleteNoteForm \



app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'development_secret_key')

# flask extensions
csrf = CSRFProtect(app)
hashing = Hashing(app)

sesh = Sesh()
validators = Validators()
user = User()
note = Note()


def before_route_load():
    url_for('static', filename='img/**/*.jpg')
    return True


@app.route('/')
def home_route():
    before_route_load()

    active_message = sesh.get_and_unset_message()
    active_errors = sesh.get_and_unset_errors()
    return render_template('home.html', 
                            sesh=sesh,
                            active_message=active_message, 
                            active_errors=active_errors)


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    before_route_load()

    ## confirm we're not logged in
    ## if we are set session message to "you gotta log out"
    ## and redirect to /logout
    if not sesh.confirm_not_logged_in():
        return redirect(url_for('logout_route'))

    form = LoginForm()

    if request.method == 'POST':

        if form.validate():

            username = form.username.data 
            password = form.password.data 
            
            ## attempt to login the username and password
            found_user = user.attempt_login(hashing, username, password);

            ## if we find a user:
            if found_user:
                ## put the username and id in the session
                sesh.set_logged_in(True)
                sesh.set_username(found_user["username"])
                sesh.set_user_id(str(found_user["_id"]))
                sesh.set_message("User logged in.")
                return redirect(url_for('dashboard_route'))
            else:
                sesh.add_error("Username or password are incorrect.")

    active_message = sesh.get_and_unset_message()
    active_errors = sesh.get_and_unset_errors()
    return render_template('login.html', 
                            sesh=sesh, 
                            active_message=active_message, 
                            active_errors=active_errors,
                            form=form) 


@app.route('/logout', methods=['GET', 'POST'])
def logout_route():
    before_route_load()

    ## confirm we're logged in
    ## if we're not redirect to /login
    if not sesh.confirm_logged_in():
        return redirect(url_for('login_route'))

    ## use the session user_id to find the user object
    found_user = user.find_by_id(ObjectId(sesh.get_user_id()))

    ## if we can't find it redirect to /login
    if not found_user:
        return redirect(url_for('login_route'))

    form = LogoutForm()

    if request.method == 'POST':
        if form.validate():
            ## logout in the user from the session
            sesh.unset_username()
            sesh.unset_user_id()
            sesh.unset_logged_in()
            sesh.set_message("User logged out.")

            ## redirect to login
            return redirect(url_for('login_route'))

    active_message = sesh.get_and_unset_message()
    active_errors = sesh.get_and_unset_errors()
    return render_template('logout.html', 
                            sesh=sesh, 
                            active_message=active_message, 
                            active_errors=active_errors,
                            form=form)


@app.route('/new_user', methods=['GET', 'POST'])
def new_user_route():
    before_route_load()

    ## confirm we're not logged in
    ## if we are set session message to "you gotta log out"
    ## and redirect to /logout
    if not sesh.confirm_not_logged_in():
        return redirect(url_for('logout_route'))

    form = NewUserForm()

    if request.method == 'POST':
        
        if form.validate():
            username = form.username.data 
            password = form.password.data 
            repeat_password = form.repeat_password.data 

            ## additional validation
            ## validate unique username
            unique_username = user.find_by_username(username)
            validators.validate_unique_username(unique_username)

            ## validate passwords match
            validators.validate_password_repeated(password, repeat_password);

            ## if any issues, push message to session errors

            ## if no addtional validation errors:
            if not sesh.get_errors():
                ## insert the user into the DB
                ## pash the hasher and the form
                user.insert_user(hashing=hashing, 
                                 username=username, 
                                 password=password)

                ## login in the user to the session
                found_user = user.attempt_login(hashing, username, password)

                if found_user:
                    sesh.set_logged_in(True)
                    sesh.set_username(found_user["username"])
                    sesh.set_user_id(str(found_user["_id"]))

                    ## redirect to update user
                    return redirect(url_for('update_user_route'))
                else:
                    sesh.set_message("Something went wrong creating the account.")

    active_message = sesh.get_and_unset_message()
    active_errors = sesh.get_and_unset_errors()
    return render_template('new_user.html', 
                            sesh=sesh, 
                            active_message=active_message, 
                            active_errors=active_errors,
                            form=form) 


@app.route('/dashboard')
def dashboard_route():
    before_route_load()

    if not sesh.confirm_logged_in():
        return redirect(url_for('login_route'))

    ## use the session user_id to find the user object
    found_user = user.find_by_id(ObjectId(sesh.get_user_id()))

    ## if we can't find it redirect to /login
    if not found_user:
        return redirect(url_for('login_route'))

    # get notes
    found_notes = note.find_by_user_id(ObjectId(sesh.get_user_id()))

    form = GoToEditNoteForm()

    active_message = sesh.get_and_unset_message()
    active_errors = sesh.get_and_unset_errors()
    return render_template('dashboard.html', 
                            sesh=sesh, 
                            active_message=active_message, 
                            active_errors=active_errors,
                            notes=found_notes,
                            form=form) 



@app.route('/update_user', methods=['GET', 'POST'])
def update_user_route():
    before_route_load()

    ## confirm we're logged in
    ## if we're not redirect to /login
    if not sesh.confirm_logged_in():
        return redirect(url_for('login_route'))

    ## use the session user_id to find the user object
    found_user = user.find_by_id(ObjectId(sesh.get_user_id()))

    if not found_user:
        return redirect(url_for('login_route'))

    form = UpdateUserForm()

    if request.method == 'GET':
        form.email.data = found_user.get('email', '')

    if request.method == 'POST':
        if form.validate():
            email = form.email.data
            if user.update_user(_id=ObjectId(sesh.get_user_id()), email=email):
                sesh.set_message("User updated!")
                return redirect(url_for('dashboard_route'))
            else:
                sesh.set_message("Nothing changed.")

    active_message = sesh.get_and_unset_message()
    active_errors = sesh.get_and_unset_errors()
    return render_template('update_user.html', 
                            sesh=sesh, 
                            active_message=active_message, 
                            active_errors=active_errors,
                            user=found_user,
                            form=form) 



@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user_route():
    before_route_load()

    ## confirm we're logged in
    ## if we're not redirect to /login
    if not sesh.confirm_logged_in():
        return redirect(url_for('login_route'))

    ## use the session user_id to find the user object
    found_user = user.find_by_id(ObjectId(sesh.get_user_id()))

    if not found_user:
        return redirect(url_for('login_route'))

    form = DeleteUserForm()

    if request.method == 'POST':

        if form.validate():
            if user.delete_user(_id=ObjectId(sesh.get_user_id())):
                note.delete_all_user_notes(user_id=ObjectId(sesh.get_user_id()))
                ## logout in the user from the session
                sesh.unset_username()
                sesh.unset_user_id()
                sesh.unset_logged_in()
                sesh.set_message("User deleted.")

                ## redirect to login
                return redirect(url_for('login_route'))
            else:
                sesh.set_message("Nothing changed.")

    active_message = sesh.get_and_unset_message()
    active_errors = sesh.get_and_unset_errors()
    return render_template('delete_user.html', 
                            sesh=sesh, 
                            active_message=active_message, 
                            active_errors=active_errors,
                            user=found_user,
                            form=form)






@app.route('/edit_note', methods=['GET', 'POST'])
def edit_note_route():
    before_route_load()

    ## confirm we're logged in
    ## if we're not redirect to /login
    if not sesh.confirm_logged_in():
        return redirect(url_for('login_route'))

    ## use the session user_id to find the user object
    found_user = user.find_by_id(ObjectId(sesh.get_user_id()))

    if not found_user:
        return redirect(url_for('login_route'))

    form = EditNoteForm()
    delete_form = DeleteNoteForm()

    found_note = None
    note_exists_in_db = True

    # if it's GET we're coming direct and have no posted id to load a note
    # so we're creating a new note
    if request.method == 'GET':
            # we don't care if the form is valid, because it's blank
            # we're not doing any DB calls
            # we just want to set note_exists_in_db to False        
            note_exists_in_db = False

    # if it's POST we're trying to insert or update a note
    # or we're coming from dashboard to start editing
    if request.method == 'POST':

        # if we have a note_id, we're either: 
        # coming from dashboard and want to populate the form with the note details;
        # or, we pressed "save" on this route and want to post an update to a note

        # get the note_id, if it exists
        note_id = request.form.get('note_id', None)

        # if note_id exists and it's not set to "new_id":
        if note_id and note_id != "new_id":

            # try to find the note using the posted note_id
            found_note = note.find_by_id(ObjectId(form.note_id.data))
            
            # if we find the note:
            if found_note:
                note_exists_in_db = True

                # get the edit_note flag, if it exists
                edit_note = request.form.get('edit_note', None)

                # if the edit note flag is set:
                if edit_note and edit_note == "true":

                    # we came from dashboard
                    # we should populate the form and that's it
                    
                    # set the form fields so the page shows correct values
                    form.note_id.data = found_note.get('_id', '')
                    delete_form.note_id.data = found_note.get('_id', '')
                    form.title.data = Markup(found_note.get('title', '')).unescape()
                    form.content.data = Markup(found_note.get('content', '')).unescape()
                    form.note_type.data = found_note.get('note_type', '')

                # if the edit flag is not set:
                else:

                    # we're trying to post an update
                    # we should update the db

                    # if form is valid:
                    if form.validate():

                        # try to update; if we succeed:
                        if note.update_note(_id=ObjectId(found_note.get('_id', '')), 
                                            title=form.title.data, 
                                            note_type=form.note_type.data, 
                                            content=form.content.data):

                            sesh.set_message("Note saved!")
                                               
                        # if update fails:
                        else:
                            sesh.set_message("Nothing changed - the note wasn't saved.")


                    # if form is not valid:
                    else:
                        sesh.set_message("Nothing changed - fix the errors below and try to update again.")

            # if we don't find the note
            else:
                sesh.set_message("Something went wrong - Couldn't find a note using the form.note_id")
                note_exists_in_db = False


        # if we posted with a "new_id" note_id:
        elif note_id and note_id == "new_id":

            # we're trying to create a new note
            # we want to attempt the insert logic

            # if form is valid:
            if form.validate():

                # try to insert the note
                inserted_id = note.insert_note(user_id=ObjectId(sesh.get_user_id()), \
                                               title=form.title.data,  \
                                               note_type=form.note_type.data, \
                                               content=form.content.data)

                # if insertion succeeded:
                if inserted_id:

                    # try to find the inserted note by the _id
                    found_note = note.find_by_id(ObjectId(inserted_id))

                    # if we found inserted note:
                    if found_note:
                        sesh.set_message("Note created!")
                        note_exists_in_db = True

                        # update hidden form fields to track _id
                        # so if we post again, we trigger update instead of insert
                        form.note_id.data = found_note.get('_id', '')
                        delete_form.note_id.data = found_note.get('_id', '')



                    # if we can't find inserted note:
                    else:
                        sesh.set_message("Something went wront - the note wasn't created.")
                        note_exists_in_db = False

                # if insertion failed:
                else:
                    sesh.set_message("Nothing changed - the note wasn't created.")
                    note_exists_in_db = False

            # if form is not valid:
            else:
                sesh.set_message("Nothing changed - fix the errors below and try to create the note again.")
                note_exists_in_db = False


        # if we have no note_id:
        elif not note_id:
            sesh.set_message("Something went wront - missing form.note_id")
            note_exists_in_db = False


    # render page
    active_message = sesh.get_and_unset_message()
    active_errors = sesh.get_and_unset_errors()
    return render_template('edit_note.html',
                            sesh=sesh,
                            active_message=active_message,
                            active_errors=active_errors,
                            user=found_user,
                            note=found_note,
                            note_exists_in_db=note_exists_in_db,
                            form=form,
                            delete_form=delete_form) 


@app.route('/delete_note', methods=['POST'])
def delete_note_route():
    if not sesh.confirm_logged_in():
        return redirect(url_for('login_route'))

    found_user = user.find_by_id(ObjectId(sesh.get_user_id()))

    if not found_user:
        return redirect(url_for('login_route'))

    delete_form = DeleteNoteForm()

    if request.method == 'POST':

        # pass on the note_id from the post
        delete_form.note_id.data = request.form.get("note_id", None)

        # validate - if not valid means missing note_id
        if delete_form.validate():

            # make sure the note belongs to the logged in user
            note_belongs_to_user = note.belongs_to_user(_id=ObjectId(delete_form.note_id.data),
                                                        user_id=ObjectId(sesh.get_user_id()))
            if note_belongs_to_user:

                # try the delete
                if note.delete_note(_id=ObjectId(delete_form.note_id.data),
                                    user_id=ObjectId(sesh.get_user_id())):
                    sesh.set_message("Note deleted.")
                
                # if delete failed:
                else:
                    sesh.set_message("Nothing changed - something went wrong deleting the note.")
            
            # if note doesn't belong to user:
            else:
                sesh.set_message("Nothing changed - that note isn't attached to your account.")

    return redirect(url_for('dashboard_route'))





@app.route('/hello')
def hello():
    return 'Hello, World'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(port=8000,debug=True)