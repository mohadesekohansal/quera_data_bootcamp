
-- Section1

SELECT platform_name as 'platform_name' , avg AS 'Average'
FROM platform JOIN
(SELECT platform_id ,AVG(num_sales) as avg 
FROM game_platform JOIN region_sales 
ON game_platform.id = region_sales.game_platform_id 
GROUP BY platform_id)t2
ON platform.id = t2.platform_id
ORDER BY avg DESC;
-- Section2

SELECT 
	game_name AS 'game_name',
    platform_name AS 'platform_name',
    release_year AS 'release_year',
    publisher_name  AS 'publisher_name',
    global_sales AS 'global_sales'
FROM game JOIN
(SELECT game_id ,platform_name ,release_year,publisher_name,global_sales
FROM publisher JOIN
(SELECT game_id ,platform_name ,release_year,publisher_id,global_sales
FROM game_publisher JOIN
(SELECT platform_name ,release_year,game_publisher_id,global_sales
FROM platform JOIN
(SELECT platform_id ,release_year, game_publisher_id,SUM(num_sales) as global_sales 
FROM game_platform JOIN region_sales 
ON game_platform.id = region_sales.game_platform_id 
GROUP BY id)t2
ON platform.id = t2.platform_id)t3
ON game_publisher.id = t3.game_publisher_id)t4
ON publisher.id = t4.publisher_id)t5
ON game.id = t5.game_id
ORDER BY global_sales DESC
LIMIT 20;

-- Section3

SELECT game_name AS 'game_name',cn AS 'platform_count' FROM game JOIN
(SELECT COUNT(DISTINCT platform_id) as cn  ,game_id
FROM game_platform JOIN game_publisher
ON game_platform.game_publisher_id = game_publisher.id
GROUP BY game_id)t2
ON game.id = t2.game_id 
WHERE cn >5
ORDER BY cn DESC, game_name;
-- Section4

SELECT 
	platform_name AS 'platform',
    genre_name AS 'genre',
    DENSE_RANK() OVER (PARTITION BY platform_name ORDER BY sale DESC) AS 'genre_in_platform_rank',
    sale as 'genre_sale',
    DENSE_RANK() OVER (ORDER BY sale DESC, platform_name , genre_name) AS 'total_rank'
FROM genre JOIN
(SELECT DISTINCT genre_id, platform_name , sum(num_sales) as sale FROM game JOIN
(SELECT game_id , platform_name , num_sales FROM game_publisher JOIN
(SELECT game_publisher_id ,platform_name , num_sales FROM platform JOIN
(SELECT game_publisher_id ,platform_id , num_sales FROM game_platform JOIN region_sales
ON region_sales.game_platform_id = game_platform.id)t2
ON platform.id = t2.platform_id)t3
ON game_publisher.id = t3.game_publisher_id)t4
ON game.id = t4.game_id
GROUP BY genre_id ,platform_name)t5
ON genre.id = t5.genre_id
ORDER BY sale DESC , platform_name , genre_name;