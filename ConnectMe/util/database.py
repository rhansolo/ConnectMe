import sqlite3

dbfile = "data/userdata.db"

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

def fetchrand():
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users ORDER BY RANDOM() LIMIT 1;")

    pf = c.fetchone()

    db.close()
    return pf
