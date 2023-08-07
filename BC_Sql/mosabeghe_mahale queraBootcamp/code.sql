-- Section1
SELECT p_title as 'p_title',title as 'c_title' FROM contests JOIN
(SELECT title as p_title ,contest_id ,cn FROM problems JOIN
(SELECT problem_id ,count(id) as cn FROM submissions GROUP BY problem_id)t2
ON problems.id = t2.problem_id) t3
ON contests.id = t3.contest_id
ORDER BY cn DESC , p_title , title;
-- Section2
SELECT title as 'title' , amount as 'amount' FROM contests JOIN
(SELECT 
	contest_id,
    sum(count(DISTINCT user_id)) OVER(partition by contest_id) as amount 
FROM problems JOIN submissions
ON problems.id = submissions.problem_id
GROUP BY contest_id )t2
ON contests.id = t2.contest_id
ORDER BY amount DESC , title ; 
-- Section3
SELECT name as 'name' ,sum(sc) as 'score' FROM users JOIN
(SELECT user_id ,problem_id ,score as sc FROM submissions WHERE problem_id in
(SELECT id FROM problems WHERE contest_id in(SELECT id FROM contests WHERE title = 'mahale'))
GROUP BY user_id , problem_id)t2
ON users.id = t2.user_id
GROUP BY user_id
ORDER BY sum(sc) DESC , name;
-- Section4
SELECT name AS 'name' ,IF(sum(sc) is null,0,sum(sc)) AS 'score' FROM users LEFT JOIN
(SELECT user_id , (score) as sc FROM submissions GROUP BY user_id , problem_id)t2
ON users.id = t2.user_id
GROUP BY user_id
ORDER BY sum(sc) DESC ,name;
-- Section5
UPDATE contests SET title = 'Mosabeghe Mahale' WHERE title = 'mahale';
-- Section6
DELETE FROM contests WHERE id not in(
SELECT contest_id 
FROM problems JOIN submissions
ON problems.id = submissions.problem_id GROUP BY contest_id);