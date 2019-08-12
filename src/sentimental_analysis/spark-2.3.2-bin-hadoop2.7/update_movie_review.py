import os
import sqlite3 as sql


class Movie:

    def __init__(self):
        "create table if doesnot exist"
        with sql.connect("../../app/data.db") as connect:
            connect.execute('''CREATE TABLE IF NOT EXISTS movies (name TEXT NOT NULL,
                    review INTEGER NOT NULL,
                    count INTEGER NOT NULL,
                    id INTEGER PRIMARY KEY AUTOINCREMENT);''')

    def register(self, movie_name):
        "register new movie"
        errorValue = 0
        try:
            with sql.connect("../../app/data.db") as connect:
                cursor = connect.cursor()
                cursor.execute(
                    "SELECT name FROM movies WHERE name ='%s';" % movie_name)
                data = cursor.fetchone()
                if data:
                    errorValue = 1
                    cursor.execute(
                        "SELECT * FROM movies WHERE name ='%s';" % movie_name)
                    data1 = cursor.fetchone()
                    print(data1)
                else:
                    cursor.execute("INSERT INTO movies(name, review, count) VALUES (?,?,?);",
                                   (movie_name, 0, 0))
                    connect.commit()
        except:
            errorValue = 2
        return errorValue

    def update_review(self, movie_name, review, count):
        errorValue = 0
        try:
            with sql.connect("../../app/data.db") as connect:
                cursor = connect.cursor()
                cursor.execute(
                    "SELECT name, review, count FROM movies WHERE name ='%s';" % movie_name)
                data = cursor.fetchone()
                review += data[1]
                count += data[2]
                if data and review >= 0:
                    cursor.execute("UPDATE movies SET review = ?, count = ? WHERE name = ?;",
                                   (review, count, movie_name))
                    connect.commit()
                    cursor.execute(
                        "SELECT name, review, count FROM movies WHERE name ='%s';" % movie_name)
                    data = cursor.fetchone()
                    print(data)
                else:
                    errorValue = 1
        except:
            errorValue = 2
        return errorValue


if __name__ == '__main__':
    movie = Movie()
    movie.register("avengers")
    movie.register("spiderman")
    movie.register("superman")
