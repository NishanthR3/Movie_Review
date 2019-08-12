import sqlite3 as sql
from passlib.hash import sha256_crypt
from flask import session

class User:

    def __init__(self):
        "create table if doesnot exist"
        with sql.connect("data.db") as connect:
            connect.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL,
                    id INTEGER PRIMARY KEY AUTOINCREMENT);''')
    
    def register(self, request):
        "register new user"
        errorValue = 0
        try:
            user, password, email = request.form['username'], request.form['password'], request.form['email']
            # hashing password
            password = sha256_crypt.encrypt(password)

            with sql.connect("data.db") as connect:
                # create a cursor object
                cursor = connect.cursor()
                cursor.execute(
                    "SELECT name FROM users WHERE name ='%s';" % user)
                data = cursor.fetchone()
                # if name already used donot create an account
                if data:
                    errorValue = 1
                else:
                    cursor.execute("INSERT INTO users(name, password,email) VALUES (?,?,?);",
                                (user, password, email))
                    connect.commit()
        except:
            errorValue = 2
        return errorValue

    def authenticate(self, request):
        "authenticate usres"
        errorValue = 1
        user, password = request.form['username'], request.form['password']
        with sql.connect("data.db") as connect:
            cursor = connect.cursor()
            cursor.execute(
                "SELECT password FROM users WHERE name ='%s';" % user)

            data = cursor.fetchone()
            # initialize status to false
            if data:
                # verify password
                if sha256_crypt.verify(password, data[0]):
                    session['username'] = user
                    session['logged_in'] = True
                    errorValue = 0
        return errorValue
