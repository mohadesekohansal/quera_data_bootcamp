-- Section1
SELECT DISTINCT
	family_name as 'family_name',
	first_name as 'name',
    birth_date as 'birth_date',
	IF((team_name = 'Serbia and Montenegro' or team_name = 'Yugoslavia'),'Serbia',team_name) as 'team_name'
FROM teams JOIN
(
	SELECT family_name , given_name AS first_name , birth_date ,team_id
	FROM players JOIN player_appearances
	ON players.player_id = player_appearances.player_id
	WHERE family_name LIKE '%ic' and team_id not in(SELECT team_id FROM teams WHERE team_name = 'Croatia') 
		and players.player_id in (SELECT player_id FROM player_appearances )
)t2
ON teams.team_id = t2.team_id
ORDER BY team_name , birth_date,family_name ,first_name;
-- Section2

   SELECT 
	team_name AS 'team_name',
    total_score AS 'total_score'
FROM teams JOIN
(SELECT
	team_id,
    CASE WHEN (team_id in(SELECT team_id FROM teams WHERE team_name = 'Germany'))
    THEN (
		(SELECT SUM(IF(position = 1 , 4 ,IF(position = 2 , 3 ,IF(position = 3 , 2 ,IF(position = 4 , 1 , 0))))) 
		FROM tournament_standings WHERE team_id in(SELECT team_id FROM teams WHERE team_name = 'West Germany'))+
        (SUM(IF(position = 1 , 4 ,IF(position = 2 , 3 ,IF(position = 3 , 2 ,IF(position = 4 , 1 , 0))))))
        )
	ELSE SUM(IF(position = 1 , 4 ,IF(position = 2 , 3 ,IF(position = 3 , 2 ,IF(position = 4 , 1 , 0)))))
	END as total_score
FROM tournament_standings
GROUP BY team_id)t2
ON teams.team_id = t2.team_id
WHERE team_name != 'West Germany'
ORDER BY total_score DESC , team_name
LIMIT 10;

-- Section3

SELECT
	full_name AS 'full_name',
	match_name AS 'match_name',
	team_name AS 'team_name',
    tournament_year AS 'tournament_year',
    age AS 'age'
FROM teams JOIN
(SELECT 
	full_name,
	match_name,
	team_id,
    SUBSTRING_INDEX(SUBSTRING_INDEX(matches.match_id,'-',2),'-',-1) as tournament_year,
    match_date-birth_day as age 
FROM matches JOIN
(SELECT CONCAT(given_name ,CONCAT(' ', family_name)) as full_name , tournament_id , match_id , team_id ,DATEDIFF(birth_date, '1970/01/01') as birth_day
FROM player_appearances JOIN players
ON player_appearances.player_id = players.player_id)t2
ON matches.match_id =  t2.match_id)t3
ON teams.team_id = t3.team_id
ORDER BY age DESC
LIMIT 20;
-- Section4
SELECT
	CONCAT(given_name ,CONCAT(' ', family_name)) AS 'full_name',
    SUM(score) as 'total_score'
FROM managers JOIN
(SELECT 
    home_team_win,
    away_team_win,
    draw,
    manager_id,
    home_team,
    CASE
		WHEN home_team = '1' and home_team_win = '1' THEN 3
		WHEN home_team = '1' and away_team_win = '1' THEN 0
		WHEN home_team = '1' and draw = '1' THEN 1
		WHEN home_team = '0' and home_team_win = '1' THEN 0
		WHEN home_team = '0' and away_team_win = '1' THEN 3
		WHEN home_team = '0' and draw = '1' THEN 1
	END as score
FROM manager_appearances JOIN matches
ON manager_appearances.match_id = matches.match_id)t2
ON managers.manager_id = t2.manager_id
GROUP BY t2.manager_id
ORDER BY SUM(score) DESC, CONCAT(given_name ,CONCAT(' ', family_name)) DESC
LIMIT 11;
