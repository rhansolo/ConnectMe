import os
import random
from random import randint
import time

from flask import Flask, redirect, url_for, render_template, session, request, flash, get_flashed_messages, send_from_directory, jsonify
from util import database

app = Flask(__name__)
app.secret_key = os.urandom(32)
user = None

def setUser(userName):
    '''
    Sets username to be passed to html files.
    '''
    global user
    user = userName


@app.route("/")
def root():
    if user in session:
    	return render_template('swipe.html', logged_in = True)
    return render_template('index.html', logged_in = False)
'''
@app.route("/login", methods=["POST"])
def login():
 	if user in session:
    	return redirect(url_for('root'))
    return render_template('login.html',logged_in = False)
'''
@app.route('/register', methods=["POST", "GET"])
def register():
    if user in session:
        return redirect(url_for('root'))
    return render_template('createprofile.html', logged_in=False)

@app.route('/questions', methods=["POST"])
def questions():
    if user in session:
        return redirect(url_for('root'))
    database.newuser(request.form["name"], request.form["email"], request.form["pswd"])
    setUser(request.form["email"])
    return render_template('questions.html', logged_in=False)

@app.route('/finalizeprofile', methods=["POST"])
def finalizeprofile():
    if user in session:
        return redirect(url_for('root'))
    database.fillqs(user, request.form["bio"], request.form["pos"], request.form["major"], request.form["interests"])
    return redirect(url_for('root'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    '''
    Checks user and pass. Makes login and register work. Checks session.
    '''
    if user in session:
        return redirect(url_for('home'))
    # instantiates DB_Manager with path to DB_FILE
    username, password, curr_page = request.form['username'], request.form['password'], request.form['address']
    # LOGGING IN
    if request.form["submit"] == "Login":
        if username != "" and password != "" and database.loginuser(username, password):
            session[username] = password
            setUser(username)
            return redirect(curr_page)
        return render_template("index.html", username = "", errors = True, alerts=["Incorrect Credentials"], logged_in = False)
    # REGISTERING
    else:
        if len(username.strip()) != 0 and not database.checkuser(username):
            if len(password.strip()) != 0:
                # add account to DB
                database.newuser(username, password)
                flash('Successfully registered account for user  "{}"'.format(username))
                return redirect(url_for('home'))
            else:
                flash('Password length insufficient')
        elif len(username) == 0:
            flash('Username length insufficient')
        else:
            flash('Username already taken!')
        # Try to register again
        return render_template('register.html', username = "", errors = True)

@app.route('/file/<path:path>')
def send_js(path):
    print(path)
    return send_from_directory('static', path)

@app.route("/api/getNextProfile")
def summary():
    profile = {
        "name": "Donald Trumpppyy " + str(randint(0, 9))
    }
    time.sleep(1)
    return jsonify(profile)
# send it back as json

if __name__ == '__main__':
    app.debug = True
    app.run()


'''
@app.route("/profile")
def profile:

@app.route("/profile/edit", methods=["POST"])
def profedit:

@app.route("/connect")
def connect:

@app.route("/message")
def msg:
'''
