import sqlite3

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
        major TEXT,
        picpath TEXT
);''')
    c.execute('''CREATE TABLE if not exists msgs (
    	id INTEGER PRIMARY KEY,
    	user1 INTEGER,
    	user2 INTEGER,
        text TEXT,
    	time TEXT
    );''')
    c.execute('''CREATE TABLE if not exists swipes (
    	id INTEGER PRIMARY KEY ,
    	user1 INTEGER,
    	user2 INTEGER
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

    swipes = getswipes(user)
    swipes = {int(s[2]) for s in swipes}

    c.execute("SELECT * FROM users WHERE username != ? ORDER BY RANDOM() LIMIT 1;", (user, ))

    pf = c.fetchall()

    for i in range(len(pf)):
        if pf[i][0] in swipes:
            pf.remove(i)

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

def swipe(user1, user2, dirr):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM swipes")
    swipes = c.fetchall()

    if dirr:
        c.execute("INSERT INTO msgs VALUES(?,?,?)", (len(usrs) + 1, user1, user2))
    else:
        c.execute("INSERT INTO msgs VALUES(?,?,?)", (-1 * (len(usrs) + 1), user1, user2))

    db.commit()
    db.close()
    return True

def getswipes(user):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM swipes WHERE user1 = ?;", (user,))
    swipes = c.fetchall()

    db.close()
    return swipes

def getuserid(user):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE username = ?;", (user,))
    uid = c.fetchone()[0]

    db.close()
    return uid

    
