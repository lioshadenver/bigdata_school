DELIMITER //

DROP PROCEDURE IF EXISTS sp_for_ETL//

CREATE PROCEDURE sp_for_ETL ()
BEGIN
    INSERT INTO moviesDB.movies (
            movie_id,
            title,
            year,
            genre,
            rating
        )
    WITH RECURSIVE cte_prepareGenres AS (
        SELECT movie_id,
               CONCAT(genres, '|') as prGenres
        FROM stagingDB.staging_movies
    ),
    cte_splitGenres AS (
        SELECT movie_id,
               LEFT(prGenres, LOCATE('|', prGenres) - 1) AS genre,
               SUBSTRING(prGenres, LOCATE('|', prGenres) + 1) AS remainingGenres
        FROM cte_prepareGenres
        UNION ALL
        SELECT movie_id,
               LEFT(remainingGenres, LOCATE('|', remainingGenres) - 1),
               SUBSTRING(remainingGenres, LOCATE('|', remainingGenres) + 1)
        FROM cte_splitGenres
        WHERE remainingGenres <> ''
    ),
    cte_moviesWithRating AS (
        SELECT m.movie_id AS movie_id,
                IF(ISNULL(REGEXP_SUBSTR(title_with_year, '\\(\\d{4}[^[:alpha:]]+$')),
                    title_with_year,
                    (LEFT(title_with_year, LOCATE(REGEXP_SUBSTR(title_with_year, '\\(\\d{4}[^[:alpha:]]+$'), title_with_year) - 2))
               ) AS title,
               RIGHT(LEFT(REGEXP_SUBSTR(title_with_year, '\\(\\d{4}[^[:alpha:]]+$'), 5), 4) AS year,
               ROUND(SUM(r.rating)/COUNT(r.rating), 1) AS rating
        FROM stagingDB.staging_movies m LEFT JOIN stagingDB.staging_ratings r
        ON m.movie_id = r.movie_id
        GROUP BY m.movie_id
    )
    SELECT mr.movie_id,
           mr.title,
           mr.year,
           sg.genre,
           mr.rating
    FROM cte_moviesWithRating mr JOIN cte_splitGenres sg
    WHERE mr.movie_id = sg.movie_id;
END//

DELIMITER ;
