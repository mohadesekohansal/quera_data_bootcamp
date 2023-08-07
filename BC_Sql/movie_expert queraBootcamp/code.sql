-- Section1
SELECT title FROM movie WHERE movie_id NOT IN(SELECT movie_id FROM movie_genres);
-- Section2
SELECT title as Title , person_name as 'Director/Leading actor' FROM person JOIN(
SELECT title , person_id FROM movie JOIN (
SELECT movie_cast.person_id as person_id , movie_cast.movie_id as movie_id FROM movie_cast INNER JOIN movie_crew 
ON movie_cast.person_id = movie_crew.person_id and movie_cast.movie_id = movie_crew.movie_id
WHERE job = 'Director' and cast_order = 0 )t2
ON movie.movie_id = t2.movie_id)t3 ON person.person_id = t3.person_id
ORDER BY title;
-- Section3
SELECT person_name as 'Name' , cn as 'count_of_movies' FROM person JOIN(
SELECT person_id , COUNT(movie_id) as cn From movie_cast WHERE cast_order = 0 GROUP BY person_id) t2
ON person.person_id = t2.person_id
ORDER BY cn DESC, person_name;
-- Section4
SELECT genre_name as genre, avg(vote_average) as avg_rating, max(vote_average) as max_rating, min(vote_average) as min_rating
FROM movie JOIN(
SELECT movie_id , genre_name FROM movie_genres JOIN genre ON movie_genres.genre_id= genre.genre_id) t2 
ON movie.movie_id = t2.movie_id GROUP BY genre_name ORDER BY avg_rating DESC;
-- Section5
SELECT person_1 as 'person #1', person_name as 'person #2' , movies_played_together as 'movies_played_together'
FROM person JOIN(
SELECT person_name as person_1, t2.person2 as person_2 , cn as movies_played_together
FROM person JOIN (
SELECT m1.person_id as person1 ,m2.person_id as person2 ,COUNT(*) as cn
FROM movie_cast as m1 JOIN movie_cast as m2 ON m1.movie_id = m2.movie_id
WHERE m1.person_id != m2.person_id and m1.person_id < m2.person_id
GROUP BY m1.person_id,m2.person_id)t2
ON person.person_id = t2.person1)t3 
ON person.person_id = t3.person_2
ORDER BY movies_played_together DESC ,person_1 ,person_name
LIMIT 10;