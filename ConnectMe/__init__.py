import os
import random
from random import randint
import datetime
from util import database as database
from flask import Flask, redirect, url_for, render_template, session, request, flash, get_flashed_messages, send_from_directory, jsonify
from util import database

database.createdb()
app = Flask(__name__)
DIR = os.path.dirname(__file__)
DIR += '/'

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
        print(database.fetchrand(user))
        return render_template('swipe.html', crtprof = False, logged_in = True, username = user)
    return render_template('index.html', crtprof = False, logged_in = False)
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
    return render_template('createprofile.html', crtprof = True, logged_in=False)

@app.route('/questions', methods=["POST"])
def questions():
    if user in session:
        return redirect(url_for('root'))
    database.newuser(request.form["name"], request.form["email"], request.form["pswd"])
    setUser(request.form["email"])
    return render_template('questions.html', crtprof = True, logged_in=False)

@app.route('/finalizeprofile', methods=["POST"])
def finalizeprofile():
    if user in session:
        return redirect(url_for('root'))
    database.fillqs(user, request.form["bio"], request.form["pos"], request.form["major"], request.form["interests"])
    return redirect(url_for('root'))

@app.route('/authenticate', methods=['POST','GET'])
def authenticate():
    '''
    Checks user and pass. Makes login and register work. Checks session.
    '''
    if user in session:
        return redirect(url_for('root'))
    # instantiates DB_Manager with path to DB_FILE
    username, password, curr_page = request.form['username'], request.form['password'], request.form['address']
    # LOGGING IN
    if request.form["submit"] == "Login":
        if username != "" and password != "" and database.loginuser(username, password):
            session['user'] = username
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
                return redirect(url_for('root'))
            else:
                flash('Password length insufficient')
        elif len(username) == 0:
            flash('Username length insufficient')
        else:
            flash('Username already taken!')
        # Try to register again
        return render_template('register.html', crtprof = True, username = "", errors = True)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop(user)
    return redirect(url_for("root"))

@app.route('/file/<path:path>')
def send_js(path):
    print(path)
    return send_from_directory('static', path)

@app.route("/api/getNextProfile")
def summary():
    randomProfile = database.fetchrand(user)
    profile = {
	"id": randomProfile[0],
        "name": randomProfile[1],
        "description": randomProfile[4],
        "status": randomProfile[5],
        "lookingFor": 'Mentor',
        "skills": ['python', 'python', 'python'],
        "interests": ['python', 'python', 'python'],
        "socials": {
            "facebook": 'https://google.com',
            "linkedin": 'https://google.com',
            "twitter": 'https://google.com',
        }
    }
    print(user in session)
    return jsonify(profile)
# send it back as json
messagesArr = []
users = {}
@app.route("/messages")
def messages():
    if 'user' in session:
        cryptoNum = random.randint(1,100000)
        users[cryptoNum] = session['user']
        print(users)
        return render_template('message.html', num=cryptoNum)

@app.route('/api/message/<num>/<message>/<time>',  methods=['GET'])
def message(num, message, time):
    messagesArr.append({
        'num': num,
        'message': message,
        'time': time
    })
    print(messagesArr)
    return jsonify({'message': 'success'})

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if user in session:
        return render_template('profile.html', crtprof = False, logged_in = True, username = user, deets=database.getuser(user))
    return redirect(url_for('root'))

@app.route('/editprofile', methods=['POST'])
def editprof():
    if user in session:
        database.edituser(request.form["name"], request.form["email"], request.form["pos"], request.form["major"], request.form["interests"], request.form["bio"], user)
        return render_template('profile.html', crtprof = False, logged_in = True, username = user, deets=database.getuser(user))
    return redirect(url_for('root'))

@app.route('/changepass', methods=['POST'])
def changepass():
    if user in session:
        if request.form['opswd'] == database.getpassword(user):
            database.resetpassword(user, request.form['pswd'])
        return render_template('profile.html', crtprof = False, logged_in = True, username = user, deets=database.getuser(user))
    return redirect(url_for('root'))

@app.route('/api/getMessages', methods=['GET'])
def getMesages():
    messagesArr = database.getmsgs(request.args["user1"], request.args["user2"])
    return jsonify(messagesArr)

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
