import sqlite3 as sql
from passlib.hash import sha256_crypt
from flask import session


class Theater:
    def __init__(self):
        "create table if doesnot exist"
        with sql.connect("data.db") as connect:
            connect.execute('''CREATE TABLE IF NOT EXISTS theatres (name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    id INTEGER PRIMARY KEY AUTOINCREMENT);''')

    def register(self, request):
        "register new theater"
        errorValue = 0
        try:
            theater, password, email, address = request.form['username'], request.form[
                'password'], request.form['email'], request.form['address']
            # hashing password
            password = sha256_crypt.encrypt(password)

            with sql.connect("data.db") as connect:
                # create a cursor object
                cursor = connect.cursor()
                cursor.execute(
                    "SELECT name FROM theatres WHERE name ='%s';" % theater)
                data = cursor.fetchone()
                # if name already used donot create an account
                if data:
                    errorValue = 1
                else:
                    cursor.execute("INSERT INTO theatres(name, password, email, address) VALUES (?,?,?,?);",
                                   (theater, password, email, address))
                    connect.commit()
        except:
            errorValue = 2
        return errorValue

    def authenticate(self, request):
        "authenticate theaters"
        errorValue = 1
        theater, password = request.form['username'], request.form['password']
        with sql.connect("data.db") as connect:
            cursor = connect.cursor()
            cursor.execute(
                "SELECT password FROM theatres WHERE name ='%s';" % theater)

            data = cursor.fetchone()
            # initialize status to false
            if data:
                # verify password
                if sha256_crypt.verify(password, data[0]):
                    session['username'] = theater
                    session['logged_in'] = True
                    session['theatre'] = True
                    errorValue = 0
        return errorValue
