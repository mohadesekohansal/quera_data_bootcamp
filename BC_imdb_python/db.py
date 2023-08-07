# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import csv
import json
import mysql.connector

data = dict()

with open("imdb_data.txt", "r") as fp:
    data = json.load(fp)

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  # password must be enterd
  password="**********"
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE imdb")

cursor.execute("USE imdb")

# +
# create table movie
cursor.execute("CREATE TABLE IF NOT EXISTS movie(id VARCHAR(8) NOT NULL,title VARCHAR(128) NOT NULL,year int NOT NULL,runtime int NOT NULL,parental_guide VARCHAR(8),gross_us_canada int,PRIMARY KEY (id))")

# create table storyline
cursor.execute("CREATE TABLE IF NOT EXISTS storyline(movie_id VARCHAR(8) NOT NULL,content text,FOREIGN KEY (movie_id) REFERENCES movie(id))")

# create table person
cursor.execute("CREATE TABLE IF NOT EXISTS person(id VARCHAR(8) NOT NULL,name VARCHAR(32) NOT NULL,PRIMARY KEY (id))")

# create table casts
cursor.execute("CREATE TABLE IF NOT EXISTS casts(id int NOT NULL AUTO_INCREMENT,movie_id VARCHAR(8) NOT NULL,person_id VARCHAR(8) NOT NULL,PRIMARY KEY (id),FOREIGN KEY (movie_id) REFERENCES movie(id),FOREIGN KEY (person_id) REFERENCES person(id))")

# create table crew
cursor.execute("CREATE TABLE IF NOT EXISTS crew(id int NOT NULL AUTO_INCREMENT,movie_id VARCHAR(8) NOT NULL,person_id VARCHAR(8) NOT NULL,role VARCHAR(8) NOT NULL,PRIMARY KEY (id),FOREIGN KEY (movie_id) REFERENCES movie(id),FOREIGN KEY (person_id) REFERENCES person(id))")

# create table genre
cursor.execute("CREATE TABLE IF NOT EXISTS genre(id int NOT NULL AUTO_INCREMENT,movie_id VARCHAR(8) NOT NULL,genre VARCHAR(16) NOT NULL,PRIMARY KEY (id),FOREIGN KEY (movie_id) REFERENCES movie(id))")


# -

cursor.reset()

# # Insertion

# +
# insert into movie table

sql_movie = "INSERT INTO movie (id, title, year, runtime, parental_guide, gross_us_canada) VALUES (%s, %s, %s, %s, %s, %s)"
val_movie = []

for i in range(1 ,251):
    id = data['title'][i-1][1]
    title = data['title'][i-1][0]
    year = int(data['year'][i-1][0])
    hour  = 0
    minute = 0
    one = 0 
    hundred = 0
    thousend = 0
    try:
        hour = int(data['runtime'][i-1][0].split('h')[0])
        try:
            minute = int(data['runtime'][i-1][0].split(' ')[1].split('m')[0])
        except:
            minute = 0 
    except:
        try:
            minute = int(data['runtime'][i-1][0].split('m')[0])
        except:
            print("ERORR")
    runtime = hour*60 + minute

    if (data['parental_guide'][i-1][0] == 'NULL'):
        parental_guide = 'Unrated'
    elif (data['parental_guide'][i-1][0] == 'null'):
        parental_guide = 'Unrated'
    elif (data['parental_guide'][i-1][0] == 'blank'):
        parental_guide = 'Unrated'
    elif (data['parental_guide'][i-1][0] == 'Not Rated'):
        parental_guide = 'Unrated'
    else:
        parental_guide = data['parental_guide'][i-1][0];
    
    try:
        one = int(data['gross_us_canada'][i-1][0].split('$')[1].split(',')[2])
        try:
            hundred = int(data['gross_us_canada'][i-1][0].split('$')[1].split(',')[1])
            try:
                thousend = int(data['gross_us_canada'][i-1][0].split('$')[1].split(',')[0])
            except:
                thousend = 0
        except:
            hundred = 0
    except:
        one = 0
    gross_us_canada = one + hundred*1000 + thousend*1000000
        
    val_movie.append((id, title, year, runtime, parental_guide, gross_us_canada))
    

# -

cursor.executemany(sql_movie, val_movie)

mydb.commit()

# +
# insert into storyline table

sql_storyline = "INSERT INTO storyline (movie_id, content) VALUES (%s, %s)"
val_storyline = []

for i in range(1 ,251):
    movie_id = data['title'][i-1][1]
    title = data['title'][i-1][0]
    content = "storyline of the "+ title + " movie"
    val_storyline.append((movie_id, content))
    
cursor.executemany(sql_storyline, val_storyline)

# +
# insert into person table

sql_person = "INSERT INTO person (id, name) VALUES (%s, %s)"
val_person = []
temp = []

for i in range(len(data['person'])):
    id = data['person'][i][0][1]
    name = data['person'][i][0][0]
    temp.append((id, name))
val_person = list(set(temp))

cursor.executemany(sql_person, val_person)

# +
# insert into casts table

sql_cast = "INSERT INTO casts (movie_id, person_id) VALUES (%s, %s)"
val_cast = []
temp = []

for i in range(len(data['title'])):
    movie_rank = data['title'][i][2]
    for j in range(len(data['person'])):
        person_rank = data['person'][j][2]
        if(movie_rank == person_rank):
            movie_id = data['title'][i][1]
            if(data['person'][j][1] == 2):
                person_id = data['person'][j][0][1]          
                temp.append((movie_id, person_id))
val_cast = list(set(temp))

cursor.executemany(sql_cast, val_cast)

# +
# insert into crew table

sql_crew = "INSERT INTO crew (movie_id, person_id, role) VALUES (%s, %s, %s)"
val_crew = []
temp = []

for i in range(len(data['title'])):
    role = ''
    movie_rank = data['title'][i][2]
    for j in range(len(data['person'])):
        person_rank = data['person'][j][2]
        if(movie_rank == person_rank):
            movie_id = data['title'][i][1]
            person_id = data['person'][j][0][1]  
            if(data['person'][j][1] == 0):
                role = 'Director'
                temp.append((movie_id, person_id,role))
            elif(data['person'][j][1] == 1):
                role = 'Writer'
                temp.append((movie_id, person_id,role))
val_crew = list(set(temp))

cursor.executemany(sql_crew, val_crew)

# +
# insert into genre table

sql_genre = "INSERT INTO genre (movie_id, genre) VALUES (%s, %s)"
val_genre = []

for i in range(len(data['genre'])):
    rank = data['genre'][i-1][1]
    for movie in data['title']:
        if(rank == movie[2]):
            genre = data['genre'][i-1][0]
            movie_id = movie[1]
    val_genre.append((movie_id,genre))

cursor.executemany(sql_genre, val_genre)
# -

mydb.commit()

cursor.close()
mydb.close()
