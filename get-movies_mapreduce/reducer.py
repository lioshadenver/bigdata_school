#! /usr/bin/env python3
from argparse import ArgumentParser
import sys


def get_args():
    '''
    function parses arguments from terminal
    '''
    parser = ArgumentParser()
    parser.add_argument(
        '-n','--number',
        type=int)
    return parser.parse_args()


def shuffling(stdin_data, num_reducers=1):
    '''
    function shuffles movies by genres and returns list of grouped (GENRE, list(MOVIE, MOVIE, ...)) values
    '''
    shuffled_movies = []

    prev_genre = None
    movies = []
    try:
        for line in stdin_data:
            genre, movie = line.split('\t')
            if genre != prev_genre and prev_genre != None:
                shuffled_movies.append((prev_genre, movies))
                movies = []
            prev_genre = genre
            movies.append(movie.rstrip())
    except:
        pass
    finally:
        shuffled_movies.append((prev_genre, movies))

    # partitioning shuffled_movies on groups
    result = []
    num_items_per_reducer = len(shuffled_movies) // num_reducers
    if len(shuffled_movies) / num_reducers != num_items_per_reducer:
        num_items_per_reducer += 1
    for i in range(num_reducers):
        result.append(shuffled_movies[num_items_per_reducer * i:num_items_per_reducer * (i+1)])
    return result


def reducing(group, num_output_movies=None):
    '''
    reduces movies according number output movies
    '''
    for genre, movies in group:
        print(f'{genre}\t{movies[0:num_output_movies]}')


def main():
    num_output_movies = get_args().number
    for group in shuffling(sys.stdin, num_reducers=1):
        reducing(group, num_output_movies)
    

if __name__ == '__main__':
    main()
