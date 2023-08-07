-- Section1
SELECT family_name , given_name as name FROM players WHERE given_name LIKE '%pir%' or family_name  LIKE '%pir%';
-- Section2
SELECT shirt_number , COUNT(*) as count_shirt_number 
FROM player_appearances
GROUP BY shirt_number 
HAVING COUNT(*) > 1000 
ORDER BY COUNT(shirt_number) DESC;
-- Section3
SELECT family_name , given_name AS name FROM players 
WHERE player_id IN (
SELECT player_id FROM award_winners 
WHERE award_id = 'A-8' and player_id = ANY(
SELECT player_id FROM award_winners WHERE award_id != 'A-8'))
ORDER BY family_name;