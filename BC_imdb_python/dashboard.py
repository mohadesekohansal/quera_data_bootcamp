import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

st.title("IMDB TOP 250 MOVIES")

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  # password must be enterd
  password="!Q2w3e4R%"
)

cursor = mydb.cursor()
cursor.execute("USE imdb")

st.header("Filtering tables")
st.subheader("Movies in a certain timeline")


cursor.execute("SELECT MIN(year) as m FROM movie")
min_year = int(cursor.fetchone()[0])
cursor.execute("SELECT MAX(year) as m FROM movie")
max_year = int(cursor.fetchone()[0])

cursor.execute("select * from movie")

movies = cursor.fetchall()

inf_year = st.number_input('Insert min year', value=0, format='%d')
sup_year = st.number_input('Insert max year', value=0, format='%d')
st.write('You want movies between years ', inf_year, ' and ', sup_year)

if sup_year < min_year:
  st.write("There is no movie")
  if inf_year > max_year:
    st.write("There is no movie")
if inf_year>sup_year:
  st.write("There is no movie")
year_limited_movie = []

for x in movies:
  if (inf_year <= x[2] and x[2] <= sup_year):
    year_limited_movie.append(x)
st.table(year_limited_movie)

st.subheader("Movies in a certain duration")

cursor.execute("SELECT MIN(runtime) as m FROM movie")
min_duration = int(cursor.fetchone()[0])
cursor.execute("SELECT MAX(runtime) as m FROM movie")
max_duration = int(cursor.fetchone()[0])

inf_duration = st.number_input('Insert min duration', value=0, format='%d')
sup_duration = st.number_input('Insert max duration', value=0, format='%d')
st.write('You want movies between duration ', inf_duration, ' and ', sup_duration)

if sup_duration < min_duration:
  st.write("There is no movie with this conditions")
  if inf_duration > max_duration:
    st.write("There is no movie with this conditions")
duration_limited_movie = []
for x in movies:
  if (inf_duration <= x[3] and x[3] <= sup_duration):
    duration_limited_movie.append(x)

st.table(duration_limited_movie)

st.subheader("Movies in a certain genre")

cursor.execute("SELECT DISTINCT genre FROM genre")
genres = cursor.fetchall()
genre_options = []
for x in genres:
  genre_options.append(x[0])

selected_genre = st.selectbox('What genre do you prefer', genre_options)

cursor.execute("SELECT movie_id, title,year,runtime,parental_guide,gross_us_canada, genre FROM movie JOIN genre ON movie.id = genre.movie_id")
genre_movie = cursor.fetchall()
genre_limited_movie =[]
for x in genre_movie:
  if(x[6] == selected_genre):
    genre_limited_movie.append(x)

st.table(genre_limited_movie)

st.subheader("Movies with your chosen stars")
cursor.execute("SELECT name,title,year,runtime,parental_guide,gross_us_canada , movie_id FROM person JOIN(SELECT title,year,runtime,parental_guide,gross_us_canada , movie_id ,person_id FROM movie JOIN casts ON movie.id = casts.movie_id)t2 ON t2.person_id = person.id")
star_movie = cursor.fetchall()
temp = []
star_options = []
for x in star_movie:
  temp.append(x[0])
star_options = list(set(temp))
selected_stars = st.multiselect('Choose your favorite stars',star_options)
star_limited_movie =[]

for x in star_movie:
  for star in selected_stars:
    if(str(x[0]) == star):
      star_limited_movie.append(x)
st.table(star_limited_movie)


st.header("Static charts")
st.subheader("10 TOP Movie Sale Bar Chart")
cursor.execute("SELECT title , gross_us_canada FROM movie ORDER BY gross_us_canada DESC limit 10")
sale_movie = cursor.fetchall()
col = []
amount = []
for x in sale_movie:
  amount.append(x[1])
  col.append(x[0])

sale_data = pd.DataFrame({'movie':amount},col)
st.bar_chart(sale_data)

st.subheader("5 TOP Active Stars Bar Chart")
cursor.execute("SELECT name , cn FROM person JOIN(SELECT person_id , COUNT(movie_id) as cn FROM movie JOIN casts ON movie.id = casts.movie_id GROUP BY person_id)t2 ON t2.person_id = person.id ORDER BY cn DESC limit 5")
active_star = cursor.fetchall()
col_star = []
amount_star = []
for x in active_star:
  amount_star.append(x[1])
  col_star.append(x[0])

active_star_data = pd.DataFrame({'star':amount_star},col_star)
st.bar_chart(active_star_data)

st.subheader("Genre Count Pie Chart")
cursor.execute("SELECT genre , COUNT(movie_id) as cn FROM genre GROUP BY genre ORDER BY cn DESC")
genre_count = cursor.fetchall()

col_genre_count = []
amount_genre_count = []

for x in genre_count:
  amount_genre_count.append(x[1])
  col_genre_count.append(x[0])

fig, ax = plt.subplots()
ax.pie(amount_genre_count, labels=col_genre_count)
st.pyplot(fig)

st.subheader("Patental Guide Count Pie Chart")

cursor.execute("SELECT parental_guide , COUNT(id) as cn FROM movie GROUP BY parental_guide ORDER BY cn DESC")
parental_guide_count = cursor.fetchall()

col_guide_count = []
amount_guide_count = []

for x in parental_guide_count:
  amount_guide_count.append(x[1])
  col_guide_count.append(x[0])

fig, ax = plt.subplots()
ax.pie(amount_guide_count, labels=col_guide_count)
st.pyplot(fig)

st.subheader("Patental Guide Count in  Each Genre Chart")

cursor.execute("SELECT t4.genre , t4.parental_guide ,cn FROM (SELECT genre ,parental_guide ,COUNT(*) as cn FROM movie JOIN genre ON movie.id = genre.movie_id GROUP BY genre , parental_guide)t3 RIGHT JOIN (SELECT * FROM (SELECT distinct genre FROM genre)t1 JOIN(SELECT distinct parental_guide FROM movie)t2)t4 ON t3.genre=t4.genre and t3.parental_guide = t4.parental_guide ORDER BY genre")
guide_per_genre = cursor.fetchall()


genre = set()
guide = set()

amount_genre_guide = []

r=[]
pg=[]
pg_13=[]
unrated=[]
g=[]
passed=[]
approved=[]
plus=[]
gp=[]
x_g=[]
tv_ma=[]
tv_pg=[]

for x in guide_per_genre:

  if(x[1] == 'R'):
    if (x[2] is None):
      r.append(0)
    else:
      r.append(x[2])
  elif(x[1] == 'PG'):
    if (x[2] is None):
      pg.append(0)
    else:
      pg.append(x[2])
  elif(x[1] == 'PG-13'):
    if (x[2] is None):
      pg_13.append(0)
    else:
      pg_13.append(x[2])
  elif(x[1] == 'Unrated'):
    if (x[2] is None):
      unrated.append(0)
    else:
      unrated.append(x[2])
  elif(x[1] == 'G'):
    if (x[2] is None):
      g.append(0)
    else:
      g.append(x[2])
  elif(x[1] == 'Passed'):
    if (x[2] is None):
      passed.append(0)
    else:
      passed.append(x[2])
  elif (x[1] == 'Approved'):
    if (x[2] is None):
      approved.append(0)
    else:
      approved.append(x[2])
  elif (x[1] == '18+'):
    if (x[2] is None):
      plus.append(0)
    else:
      plus.append(x[2])
  elif (x[1] == 'GP'):
    if (x[2] is None):
      gp.append(0)
    else:
      gp.append(x[2])
  elif (x[1] == 'X'):
    if (x[2] is None):
      x_g.append(0)
    else:
      x_g.append(x[2])
  elif (x[1] == 'TV-MA'):
    if (x[2] is None):
      tv_ma.append(0)
    else:
      tv_ma.append(x[2])
  elif (x[1] == 'TV-PG'):
    if (x[2] is None):
      tv_pg.append(0)
    else:
      tv_pg.append(x[2])

  genre.add(x[0])
  guide.add(x[1])
  amount_genre_guide.append(x[2])

genre_guide_df3 = pd.DataFrame({
  'R':np.array(r),
  'PG':np.array(pg),
  'PG-13':np.array(pg_13),
  'Unrated':np.array(unrated),
  'G':np.array(g),
  'Passed':np.array(passed),
  'Approved':np.array(approved),
  '18+':np.array(plus),
  'GP':np.array(gp),
  'X':np.array(x_g),
  'TV-MA':np.array(tv_ma),
  'TV-PG':np.array(tv_pg)}
  ).set_index(pd.Index(sorted(genre)))

st.bar_chart(genre_guide_df3)

st.header("Interactive charts")
selected_genre_sale = st.selectbox('What genre do you want', genre_options)

cursor.execute("SELECT title , gross_us_canada ,genre FROM movie JOIN genre ON genre.movie_id = movie.id ORDER BY gross_us_canada DESC")
genre_sale = cursor.fetchall()
col_genre = []
amount_genre = []
for x in genre_sale:
  if(x[2] == selected_genre_sale):
    amount_genre.append(x[1])
    col_genre.append(x[0])

sale_genre_data = pd.DataFrame({'movie':amount_genre},col_genre)
st.bar_chart(sale_genre_data)
