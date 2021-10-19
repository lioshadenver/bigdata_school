DROP TABLE IF EXISTS staging_movies;

CREATE TABLE staging_movies (
    movie_id INT NOT NULL,
    title_with_year VARCHAR(255) NOT NULL,
    genres VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (movie_id)
);
