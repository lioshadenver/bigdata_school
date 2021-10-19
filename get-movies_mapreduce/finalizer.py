#! /usr/bin/env python3
import sys


def print_result(genre, movies):
    '''
    prints movies to csv like format
    '''
    for movie in movies[2:-3].split("', '"):
        movie_title, movie_year = movie[1:-1].rsplit(',', maxsplit=1)
        print(f'{genre};{movie_title};{movie_year}')


def main():
    for line in sys.stdin:
        genre, movies = line.split('\t')
        print_result(genre, movies)


if __name__ == '__main__':
    main()
