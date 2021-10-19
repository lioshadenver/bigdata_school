DROP TABLE IF EXISTS staging_ratings;

CREATE TABLE staging_ratings (
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    rating DECIMAL(2,1) DEFAULT NULL,
    PRIMARY KEY (user_id, movie_id)
);
