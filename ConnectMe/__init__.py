import os
import random
from random import randint
import datetime

from flask import Flask, redirect, url_for, render_template, session, request, flash, get_flashed_messages, send_from_directory, jsonify
# from util import database
# ---------------------------------------------------------

import sqlite3
#c.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?)", (0, name, user, password, "", "", "", ""))
dbfile = "data/userdata.db"
def createdb():
    db = initdb()
    c = db.cursor()
    c.execute('''CREATE TABLE if not exists users (
	id INTEGER PRIMARY KEY,
	name TEXT,
	username TEXT,
	password TEXT,
	bio TEXT,
	position TEXT,
	interests TEXT,
    major TEXT
);''')
    c.execute('''CREATE TABLE if not exists msgs (
    	id integer PRIMARY KEY AUTOINCREMENT,
    	user1 integer,
    	user2 integer,
        text TEXT,
    	time datetime
    );''')
    db.commit()
    db.close()

def initdb():
    db = sqlite3.connect(dbfile)
    return db

def checkuser(user):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE username = ?", (user, ))
    dupusers = c.fetchall()

    db.close()

    return len(dupusers) > 0

def getpassword(user):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT password FROM users WHERE username = ?", (user, ))
    password = c.fetchone()[0]

    db.close()

    return password

def resetpassword(user, newpass):
    db = initdb()
    c = db.cursor()

    c.execute("UPDATE users SET password = ? WHERE username = ?", (newpass, user))

    db.commit()
    db.close()

def loginuser(user, password):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (user, password))
    creds = c.fetchall()

    db.close()

    return len(creds) > 0

def newuser(name, user, password):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users")
    usrs = c.fetchall()
    if len(usrs) == 0:
        c.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?)", (0, name, user, password, "", "", "", ""))
    else:
        c.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?,?)", (len(usrs), name, user, password, "", "", "", ""))

    db.commit()
    db.close()

    return True

def fillqs(email, bio, pos, maj, intrsts):
    db = initdb()
    c = db.cursor()

    c.execute("UPDATE users SET bio = ?, position = ?, interests = ?, major = ? WHERE username = ?", (bio, pos, intrsts, maj, email))

    db.commit()
    db.close()

    return True

def fetchrand(user):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users  WHERE username != ? ORDER BY RANDOM() LIMIT 1;", (user, ))

    pf = c.fetchone()

    db.close()
    return pf

def getuser(user):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE username = ?;", (user, ))

    pf = c.fetchone()

    db.close()
    return pf

def edituser(name, user, pos, maj, intrsts, bio, olduser):
    db = initdb()
    c = db.cursor()

    c.execute("UPDATE users SET name = ?, username = ?, bio = ?, position = ?, interests = ?, major = ? WHERE username = ?", (name, user, bio, pos, intrsts, maj, user))

    db.commit()
    db.close()

    return True

def getmsgs(user1, user2):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM msgs WHERE user1 = ? AND user2 = ?", (user1, user2))

    msgs = c.fetchall()

    c.execute("SELECT * FROM msgs WHERE user1 = ? AND user2 = ?", (user2, user1))

    msgs.extend(c.fetchall())

    db.close()
    return msgs

def addmsg(txt, user1, user2):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM msgs")
    msgs = c.fetchall()

    if len(msgs) == 0:
        c.execute("INSERT INTO msgs VALUES(?,?,?,?,?)", (0, user1, user2, content, str(datetime.now())))
    else:
        c.execute("INSERT INTO msgs VALUES(?,?,?,?,?)", (len(usrs), user1, user2, content, str(datetime.now())))

    db.commit()
    db.close()
    return msgs
# ---------------------------------------------------------

createdb()
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
        print(fetchrand(user))
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
    newuser(request.form["name"], request.form["email"], request.form["pswd"])
    setUser(request.form["email"])
    return render_template('questions.html', crtprof = True, logged_in=False)

@app.route('/finalizeprofile', methods=["POST"])
def finalizeprofile():
    if user in session:
        return redirect(url_for('root'))
    fillqs(user, request.form["bio"], request.form["pos"], request.form["major"], request.form["interests"])
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
        if username != "" and password != "" and loginuser(username, password):
            session['user'] = username
            session[username] = password
            setUser(username)
            return redirect(curr_page)
        return render_template("index.html", username = "", errors = True, alerts=["Incorrect Credentials"], logged_in = False)
    # REGISTERING
    else:
        if len(username.strip()) != 0 and not checkuser(username):
            if len(password.strip()) != 0:
                # add account to DB

                newuser(username, password)
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
    randomProfile = fetchrand(user)
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
        return render_template('profile.html', crtprof = False, logged_in = True, username = user, deets=getuser(user))
    return redirect(url_for('root'))

@app.route('/editprofile', methods=['POST'])
def editprof():
    if user in session:
        edituser(request.form["name"], request.form["email"], request.form["pos"], request.form["major"], request.form["interests"], request.form["bio"], user)
        return render_template('profile.html', crtprof = False, logged_in = True, username = user, deets=getuser(user))
    return redirect(url_for('root'))

@app.route('/changepass', methods=['POST'])
def changepass():
    if user in session:
        if request.form['opswd'] == getpassword(user):
            resetpassword(user, request.form['pswd'])
        return render_template('profile.html', crtprof = False, logged_in = True, username = user, deets=getuser(user))
    return redirect(url_for('root'))

@app.route('/api/getMessages', methods=['GET'])
def getMesages():
    messagesArr = getmsgs(request.args["user1"], request.args["user2"])
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
