import os
from mysql.connector import connect
import pandas as pd
from my_logger import get_logger
from env import CSV_MOVIES_FILE_PATH, DB_CONFIGURATION, STAGING_DB_NAME, STG_MOVIES_TABLE_NAME


def main():
    logger = get_logger()
    read_and_load_data_to_stagingDB(logger)


def read_and_load_data_to_stagingDB(logger):
    '''
    function reads data from csv and loads it to staging database  
    '''
    try:
        dtype = {
            'movieId':'int32',
            'title':'string',
            'genres':'string',
        }
        logger.info('Starting loading movies to the stagingDB')
        connection = connect(database=STAGING_DB_NAME, **DB_CONFIGURATION)
        with connection.cursor() as cursor:
            csv_movies_file_path = os.path.join(os.getcwd(), CSV_MOVIES_FILE_PATH)
            insert_in_table_query = f'INSERT INTO {STG_MOVIES_TABLE_NAME} (movie_id, title_with_year, genres) VALUES (%s, %s, %s)'
            for chunk in pd.read_csv(csv_movies_file_path, 
                                     usecols=['movieId', 'title', 'genres'],
                                     sep=',', dtype=dtype, chunksize=10000):

                data = list(zip(chunk['movieId'],
                                chunk['title'],
                                chunk['genres']))
                cursor.executemany(insert_in_table_query, data)
                connection.commit()
    except Exception as err:
        logger.error(f'error in read_and_load_data_to_stagingDB() function. Error massage: {err}')
        connection.rollback()
    else:
        logger.info('Ending loading movies to the stagingDB')
    finally:
        connection.close()


if __name__ == '__main__':
    main()
