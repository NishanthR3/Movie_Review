import sqlite3 as sql
from passlib.hash import sha256_crypt
from flask import session

class Movie:
    def __init__(self):
        "create table if doesnot exist"
        with sql.connect("data.db") as connect:
            connect.execute('''CREATE TABLE IF NOT EXISTS movies (name TEXT NOT NULL,
                    review INTEGER NOT NULL,
                    count INTEGER NOT NULL,
                    movie_id INTEGER PRIMARY KEY AUTOINCREMENT);''')

    def add_movie(self, movie_name):
        "add new movie"
        errorValue = 0
        try:
            with sql.connect("data.db") as connect:
                # create a cursor object
                cursor = connect.cursor()
                cursor.execute(
                    "SELECT name FROM movies WHERE name ='%s';" % movie_name)
                data = cursor.fetchone()
                # if name already used donot create 
                if data:
                    errorValue = 1
                else:
                    cursor.execute("INSERT INTO movies(name, review, count) VALUES (?,?,?);",
                                   (movie_name, 0, 0))
                    connect.commit()
        except:
            errorValue = 2
        return errorValue

    def movies_list(self):
        "retrieve all movies"
        errorValue = 0
        try:
            with sql.connect("data.db") as connect:
                # create a cursor object
                cursor = connect.cursor()
                cursor.execute(
                    "SELECT * FROM movies;")
                data = cursor.fetchall()
                if not data:
                    errorValue = 1

                # data.sort(key=lambda x: x['review'] / x['count'])
        except:
            errorValue = 2
        
        return (errorValue, data)
