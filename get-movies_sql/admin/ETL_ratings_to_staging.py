import os
from mysql.connector import connect
import pandas as pd
from my_logger import get_logger
from env import CSV_RATINGS_FILE_PATH, DB_CONFIGURATION, STAGING_DB_NAME, STG_RATINGS_TABLE_NAME


def main():
    logger = get_logger()
    read_and_load_data_to_stagingDB(logger)


def read_and_load_data_to_stagingDB(logger):
    '''
    function reads data from csv and loads it to staging database 
    '''
    try:
        dtype = {
            'userId':'int32',
            'movieId':'int32',
            'rating':'float16',
        }
        logger.info('Starting loading ratings to the stagingDB')
        connection = connect(database=STAGING_DB_NAME, **DB_CONFIGURATION)
        with connection.cursor() as cursor:
            csv_ratings_file_path = os.path.join(os.getcwd(), CSV_RATINGS_FILE_PATH)
            insert_in_table_query = f'INSERT INTO {STG_RATINGS_TABLE_NAME} (user_id, movie_id, rating) VALUES (%s, %s, %s)'
            for chunk in pd.read_csv(csv_ratings_file_path, 
                                     usecols=['userId', 'movieId', 'rating'],
                                     sep=',', dtype=dtype, chunksize=10000):

                data = list(zip(chunk['userId'],
                                chunk['movieId'],
                                chunk['rating']))
                cursor.executemany(insert_in_table_query, data)
                connection.commit()
    except Exception as err:
        logger.error(f'error in read_and_load_data_to_stagingDB() function. Error massage: {err}')
        connection.rollback()
    else:
        logger.info('Ending loading ratings to the stagingDB')
    finally:
        connection.close()


if __name__ == '__main__':
    main()
