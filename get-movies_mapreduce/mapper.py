#! /usr/bin/env python3
from argparse import ArgumentParser
import csv
import sys
import re


def get_args():
    '''
    function parses arguments from terminal
    '''
    parser = ArgumentParser()
    parser.add_argument(
        '-r', '--regexp')
    parser.add_argument(
        '-yf', '--year-from',
        type=int)
    parser.add_argument(
        '-yt', '--year-to',
        type=int)
    parser.add_argument(
        '-g', '--genres')
    return parser.parse_args()


def mapping(line, line_number, args):
    '''
    function filters movies and output them in stdout in "GENRE\t(TITLE,YEAR)" format
    '''
    _, title_with_year, movies_genres = line
    movies_genres = movies_genres.split('|')

    # filtering movies according to genres
    if args.genres:
        needed_genres = []
        for genre in (args.genres).split('|'):
            if not genre.lower() in map(lambda g: g.lower(), movies_genres):
                continue
            else:
                needed_genres.append(genre.capitalize())
        if not needed_genres:
            return
    else:
        if movies_genres[0] == '(no genres listed)':
            movies_genres = [None]
        needed_genres = movies_genres
        
    # filtering movies according to year and regexp
    try:
        movie_year = re.search(r'(?<=\()\d{4}(?=[^a-zA-Z]*\))', title_with_year)
        year_index = movie_year.start() - 1
        movie_title = title_with_year[:year_index].rstrip(' ')
        movie_year = int(movie_year.group())
    except AttributeError as err:
        movie_year = None
        movie_title = title_with_year
    
    if args.year_from:
        if not movie_year or movie_year < args.year_from:
            return
    if args.year_to:
        if not movie_year or movie_year > args.year_to:
            return
    if args.regexp:
        pattern = args.regexp
        if not re.search(pattern, movie_title):
            return

    for movie_genre in needed_genres:
        print(f'{movie_genre}\t("{movie_title}",{movie_year})')


def main():
    args = get_args()
    for line_number, line in enumerate(csv.reader(sys.stdin)):
        if line_number == 0:
            continue
        mapping(line, line_number, args)


if __name__ == "__main__":
    main()
