#! /usr/bin/env python3
from argparse import ArgumentParser
from collections import defaultdict
from logging import StreamHandler, Formatter
import logging
import sys
import csv
import re


MOVIES_FILE_PATH = './data/movies.csv'
RATINGS_FILE_PATH = './data/ratings.csv'


def get_args():
    '''
    function parses arguments from terminal
    '''
    parser = ArgumentParser(description='Commandline app for searching movies')
    parser.add_argument(
        '-n','--number',
        metavar='NUMBER',
        type=int,
        help='the number of the best rated movies to output')
    parser.add_argument(
        '-r', '--regexp',
        metavar='REGEXP',
        help='regular expression for searching by movie name')
    parser.add_argument(
        '-yf', '--year-from',
        metavar='YEAR',
        type=int,
        help='sets the year for starting the search')
    parser.add_argument(
        '-yt', '--year-to',
        metavar='YEAR',
        type=int,
        help='sets the year for finishing the search')
    parser.add_argument(
        '-g', '--genres',
        metavar='"GENRE|GENRE|..."',
        help='sets the genre/genres to search')
    return parser.parse_args()


def main():
    args = get_args()
    logger = get_logger()
    movies, all_ganres = get_movies_and_list_all_ganres(args, logger)
    ratings = get_rating(movies, logger)
    sort_and_print_movies(args, movies, ratings, all_ganres, logger)


def get_logger():
    '''
    function creates and returns logger. Logger output error mesagges in STDUOT
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = StreamHandler(stream=sys.stdout)
    handler.setFormatter(Formatter(fmt=
        '[%(asctime)s: %(levelname)s] %(message)s'))  # messages format
    logger.addHandler(handler)
    return logger


def get_movies_and_list_all_ganres(args, logger):
    '''
    function filters and returns movies according to request;
    returns tuple of movies dictionary and set of all movie genres that occur
    '''
    try:
        movies = {}
        all_movies_genres = set()
        file = open(MOVIES_FILE_PATH, 'r')
        reader = csv.reader(file)

        for number, row in enumerate(reader):
            if number == 0:
                continue
            id, movie_name_with_year, genres = row
            movies_genres = genres.split('|')
            all_movies_genres.update(movies_genres)
            try:
                year = re.search(r'(?<=\()\d{4}(?=[^a-zA-Z]*\))', movie_name_with_year)
                year_index = year.start() - 1
                movie_name = movie_name_with_year[:year_index].rstrip(' ')
                year = int(year.group())
            except AttributeError as err:
                year = 0
                movie_name = movie_name_with_year

            # filtering movies according to request
            if args.year_from:
                if not year:
                    continue
                if year < args.year_from:
                    continue
            if args.year_to:
                if not year:
                    continue
                if year > args.year_to:
                    continue
            if args.regexp:
                pattern = args.regexp
                if not re.search(pattern, movie_name):
                    continue
            if args.genres:
                needed_genres = []
                for genre in (args.genres).split('|'):
                    if not genre.lower() in map(lambda g: g.lower(), movies_genres):
                        continue
                    else:
                        needed_genres.append(genre)
                        continue
                if not needed_genres:
                    continue
            else:
                if movies_genres[0] == '(no genres listed)':
                    movies_genres = ['None']
                needed_genres = movies_genres

            movies[id] = (movie_name, year, needed_genres)
    except ArithmeticError as err:
        logger.debug('error in get_movies_and_list_all_ganres() function. Error massage: %s' %err)
    finally:
        file.close()
    return movies, all_movies_genres


def get_rating(movies, logger):
    '''
    function counts and return rating for required movies;
    returns dictionary where key is movie id, value is rating
    '''
    ratings_counter = defaultdict(lambda: [float(), int()])
    try:
        file = open(RATINGS_FILE_PATH, 'r')
        reader = csv.reader(file)
        
        for number, row in enumerate(reader):
            if number == 0:
                continue
            _, movie_id, rating, _ = row
            if not movie_id in movies.keys():
                continue
            ratings_and_count = ratings_counter[movie_id]
            ratings_and_count[0] += float(rating)
            ratings_and_count[1] += 1

        ratings = {movie_id: round(ratings_and_count[0]/ratings_and_count[1], 1)
                   for movie_id, ratings_and_count in ratings_counter.items()}
    except Exception as err:
        logger.debug('error in get_rating() function. Error massage: %s' %err)
    finally:
        file.close()
    return ratings


def sort_and_print_movies(args, movies, ratings, all_ganres, logger):
    '''
    function sorts and output movies according to request
    '''
    try:
        if args.genres:
            needed_genres = (args.genres).split('|')
        else:
            no_genre = []
            needed_genres = []
            for genre in all_ganres:
                if genre == '(no genres listed)':
                    no_genre.append('None')
                    continue
                needed_genres.append(genre)
            needed_genres.sort()
            needed_genres += no_genre

        is_output_movies = False    
        for needed_genre in needed_genres:
            counter = 0
                                                            # sorted by ratings first, then by year
            for movie_id, rating in sorted(ratings.items(), key=lambda i: (i[1], movies[i[0]][1]), reverse=True):
                if counter == args.number:
                    break            
                movie_name, year, genres = movies[movie_id]
                if year == 0:
                    year = None
                for genre in genres:
                    if genre == needed_genre:
                        print(f'{genre.capitalize()},"{movie_name}",{year},{rating}')
                        genres.remove(genre)
                        counter += 1
                        is_output_movies = True
        if not is_output_movies:
            logger.info('movies not found')
    except Exception as err:
        logger.debug('error in sort_and_print_movies() function. Error massage: %s' %err)


if __name__ == '__main__':
    main()
