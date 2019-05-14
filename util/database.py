import sqlite3

dbfile = "data/userdata.db"

def initdb():
    db = sqlite3.connect(dbfile)
    return db

def checkuser(user):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE name = ?", (user, ))
    dupusers = c.fetchall()

    db.close()

    return len(dupusers) > 0

def getpassword(user):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT password FROM users WHERE name = ?", (user, ))
    password = c.fetchone()[0]

    db.close()

    return password

def resetpassword(user, newpass):
    db = initdb()
    c = db.cursor()

    c.execute("UPDATE users SET password = ? WHERE name = ?", (newpass, user))

    db.commit()
    db.close()

def loginuser(user, password):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users WHERE name = ? AND password = ?", (user, password))
    creds = c.fetchall()

    db.close()

    return len(creds) > 0

def newuser(name, user, password):
    db = initdb()
    c = db.cursor()

    c.execute("SELECT * FROM users")
    usrs = c.fetchall()
    if len(usrs) == 0:
        c.execute("INSERT INTO users VALUES(?,?)", (0, name, user, password, "", "", "", "", ""))
    else:
        c.execute("INSERT INTO users VALUES(?,?)", (len(usrs), name, user, password, "", "", "", "", ""))

    db.commit()
    db.close()

    return True

# def fillqs():
