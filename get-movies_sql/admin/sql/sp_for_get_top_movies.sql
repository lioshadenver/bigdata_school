DELIMITER //

DROP PROCEDURE IF EXISTS sp_get_top_movies//

CREATE PROCEDURE sp_get_top_movies (
    IN n INT,
    IN regex VARCHAR(100),
    IN year_from INT,
    IN year_to INT,
    IN genres VARCHAR(200)
    )
BEGIN

WITH cte_movies AS (
	SELECT
		genre,
        title,
        year,
        rating,
        ROW_NUMBER() OVER(PARTITION BY genre ORDER BY rating DESC, genre, year DESC) AS row_num
	FROM movies m
	WHERE
        IF(regex = '', 1, REGEXP_LIKE(title, regex, 'c'))
		AND IF(year_from = 0, 1, year >= year_from)
		AND IF(year_to = 0, 1, year <= year_to)
        AND	IF(genres = '', 1, FIND_IN_SET(genre, genres))
) SELECT
	genre,
	title,
	year,
	rating
FROM cte_movies
WHERE row_num <= IF(n = -1, (SELECT COUNT(DISTINCT(movie_id)) FROM movies), n);

END//

DELIMITER ;