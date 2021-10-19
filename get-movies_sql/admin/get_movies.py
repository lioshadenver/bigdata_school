#! /usr/bin/env python3
from argparse import ArgumentParser
from mysql.connector import connect
from my_logger import get_logger
from env import MAIN_DB_NAME, DB_CONFIGURATION, SP_FOR_GET_MOVIES_NAME


def get_args():
    '''
    function parses arguments from terminal
    '''
    parser = ArgumentParser(description='Commandline app for searching movies')
    parser.add_argument(
        '-n','--number',
        metavar='NUMBER',
        type=int,
        default='-1',
        help='the number of the best rated movies to output')
    parser.add_argument(
        '-r', '--regexp',
        metavar='REGEXP',
        default='',
        help='regular expression for searching by movie name')
    parser.add_argument(
        '-yf', '--year-from',
        metavar='YEAR',
        type=int,
        default='0',
        help='sets the year for starting the search')
    parser.add_argument(
        '-yt', '--year-to',
        metavar='YEAR',
        type=int,
        default='0',
        help='sets the year for finishing the search')
    parser.add_argument(
        '-g', '--genres',
        metavar='"GENRE|GENRE|..."',
        default='',
        help='sets the genre/genres to search')
    return parser.parse_args()


def main():
    args = get_args()
    logger = get_logger()
    call_sp_and_print_result(logger, args)


def call_sp_and_print_result(logger, args):
    '''
    function calls sql stored procedure, gets result movies set and print it
    '''
    try:
        with connect(database=MAIN_DB_NAME, **DB_CONFIGURATION) as connection:
            with connection.cursor() as cursor:
                proc_args = (args.number, args.regexp, args.year_from, args.year_to, args.genres.replace('|', ','))
                cursor.callproc(SP_FOR_GET_MOVIES_NAME, proc_args)
                
                is_output_movies = False
                for result in cursor.stored_results():
                    for genre, title, year, rating in result.fetchall():
                        print(f'{genre},"{title}",{year},{rating}')
                        is_output_movies = True
        if not is_output_movies:
            logger.info('movies not found')
    except Exception as err:
        logger.error('error in call_sp_and_get_movies() function. Error massage: %s' %err)


if __name__ == '__main__':
    main()
