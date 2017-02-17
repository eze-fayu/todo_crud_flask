import os
from flask import Flask, session, escape, \
    send_from_directory, url_for, render_template, \
    request, abort, redirect
from flask_hashing import Hashing
from bson.objectid import ObjectId

import functions as Functions
from user import User
from note import Note
from sesh import Sesh
from validators import Validators
from models import Models


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'development_secret_key')

hashing = Hashing(app)

sesh = Sesh()
validators = Validators()
models = Models()
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

    if request.method == 'POST':
        ## validate presence of needed fields
        required_fields = ["username", "password"]
        validators.validate_presences(request.form, required_fields);

        ## if any issues, push message to session errors

        ## if no errors:
        if not sesh.get_errors():

            username = request.form["username"];
            password = request.form["password"];
            
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
                            sesh=sesh, active_message=active_message, active_errors=active_errors) 


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

    if request.method == 'POST':

        ## validate presence of needed fields
        required_fields = ["logout"]
        validators.validate_presences(request.form, required_fields);

        ## if no errors:
        if not sesh.get_errors():
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
                            active_errors=active_errors)


@app.route('/new_user', methods=['GET', 'POST'])
def new_user_route():
    before_route_load()

    ## confirm we're not logged in
    ## if we are set session message to "you gotta log out"
    ## and redirect to /logout
    if not sesh.confirm_not_logged_in():
        return redirect(url_for('logout_route'))

    if request.method == 'POST':
        
        ## validate presence of needed fields
        required_fields = ["username", "password", "repeat-password"]
        validators.validate_presences(request.form, required_fields);

        ## validate username max length
        fields_with_max_lengths = [{ "username" : 30 }]
        validators.validate_max_lengths(request.form, fields_with_max_lengths);

        ## validate unique username
        ## TODO

        ## validate passwords match
        validators.validate_password_repeated(request.form["password"], request.form["repeat-password"]);

        ## if any issues, push message to session errors

        ## if no errors:
        if not sesh.get_errors():
            ## insert the user into the DB
            ## pash the hasher and the form
            user.insert_user(hashing=hashing, form=request.form)

            ## login in the user to the session
            found_user = user.attempt_login(hashing, request.form["username"], request.form["password"])

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
                            active_errors=active_errors) 


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

    active_message = sesh.get_and_unset_message()
    active_errors = sesh.get_and_unset_errors()
    return render_template('dashboard.html', 
                            sesh=sesh, 
                            active_message=active_message, 
                            active_errors=active_errors,
                            notes=found_notes) 



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

    if request.method == 'POST':
        ## validate presence of needed fields
        required_fields = ["email", "_id"]
        validators.validate_presences(request.form, required_fields);

        if not sesh.get_errors():
            if user.update_user(form=request.form, _id=ObjectId(sesh.get_user_id())):
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
                            user=found_user) 



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

    if request.method == 'POST':

        ## validate presence of needed fields
        required_fields = ["delete", "_id"]
        validators.validate_presences(request.form, required_fields);

        ## if no errors:
        if not sesh.get_errors():
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
                            user=found_user)




@app.route('/edit_note', methods=['GET', 'POST'])
def edit_note_route():
    before_route_load()
    note_exists_in_db = True
    ## confirm we're logged in
    ## if we're not redirect to /login
    if not sesh.confirm_logged_in():
        return redirect(url_for('login_route'))

    ## use the session user_id to find the user object
    found_user = user.find_by_id(ObjectId(sesh.get_user_id()))

    if not found_user:
        return redirect(url_for('login_route'))

    ## if it's get we're coming from dashboard (or direct)
    if request.method == 'GET':
        if request.args.get('id'):
            # if we have an id,
            # and it belongs to this user,
            # find note and pre-fill form
            found_note = note.find_by_id(ObjectId(request.args.get('id')))
            if not found_note:
                sesh.set_message("Couldn't find the note you're looking for.")
        else:
            # new note
            found_note = {
                "title" : "",
                "content" : "",
                "type": ""
            }
            note_exists_in_db = False

    ## if it's post we're trying to save our note
    ## it may be an update or it may be an insert
    if request.method == 'POST':
         ## validate presence of needed fields
        required_fields = ["title", "content"]
        validators.validate_presences(request.form, required_fields);

        ## validate username max length
        fields_with_max_lengths = [{ "content" : 1000 }]
        validators.validate_max_lengths(request.form, fields_with_max_lengths);

        if not sesh.get_errors():
            ## if we have an _id on the form it means it's an update
            if request.form.get("_id"):
                found_note = note.find_by_id(ObjectId(request.form.get("_id")))
                if found_note:
                    if note.update_note(form=request.form, _id=ObjectId(request.form.get("_id"))):
                        sesh.set_message("Note saved!")
                        found_note = note.find_by_id(ObjectId(request.form.get("_id")))
                    else:
                        sesh.set_message("Nothing changed - the note wasn't saved.")
                else:
                    sesh.set_message("Couldn't find the note you're looking for.")

            
            ## if we have no _id on the form it's new and an insert
            else:
                found_note = {
                    "title" : request.form.get('title', ""),
                    "content" : request.form.get('content', ""),
                    "type" : request.form.get('type', "")
                }
                inserted_id = note.insert_note(form=request.form, user_id=ObjectId(sesh.get_user_id()))
                if inserted_id:
                    found_note = note.find_by_id(ObjectId(inserted_id))
                    if found_note:
                        sesh.set_message("Note created!")
                    else:
                        sesh.set_message("Something went wront - the note wasn't created.")
                else:
                    sesh.set_message("Nothing changed - the note wasn't created.")
                    note_exists_in_db = False
        else:
            if request.form.get("_id"):
                found_note = note.find_by_id(ObjectId(request.form.get("_id")))
            else:
                found_note = {
                    "title" : request.form.get('title', ""),
                    "content" : request.form.get('content', ""),
                    "type" : request.form.get('type', "")
                }
                note_exists_in_db = False


      
    active_message = sesh.get_and_unset_message()
    active_errors = sesh.get_and_unset_errors()
    return render_template('edit_note.html', 
                            sesh=sesh, 
                            active_message=active_message, 
                            active_errors=active_errors,
                            user=found_user,
                            note=found_note,
                            note_exists_in_db=note_exists_in_db,
                            note_model=models.get_note_model()) 




@app.route('/delete_note', methods=['POST'])
def delete_note_route():
    if not sesh.confirm_logged_in():
        return redirect(url_for('login_route'))

    found_user = user.find_by_id(ObjectId(sesh.get_user_id()))

    if not found_user:
        return redirect(url_for('login_route'))

    if request.method == 'POST':
        ## validate presence of needed fields
        required_fields = ["delete", "_id"]
        validators.validate_presences(request.form, required_fields);

        ## if no errors:
        if not sesh.get_errors():
            if note.delete_note(form=request.form, 
                                _id=ObjectId(request.form['_id']),
                                user_id=ObjectId(sesh.get_user_id())):
                sesh.set_message("Note deleted.")
            else:
                sesh.set_message("Nothing changed.")

    return redirect(url_for('dashboard_route'))





@app.route('/hello')
def hello():
    return 'Hello, World'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(port=8000,debug=True)