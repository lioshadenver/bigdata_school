#! /bin/bash

staging_db_name='stagingDB'
main_db_name='moviesDB'

path_to_create_stg_db_script='./admin/sql/create_stagingDB.sql'
path_to_create_stg_movies_table_script='./admin/sql/create_stg_movies_table.sql'
path_to_create_stg_ratings_table_script='./admin/sql/create_stg_ratings_table.sql'
path_to_create_main_db_script='./admin/sql/create_moviesDB.sql'
path_to_create_main_movies_table_script='./admin/sql/create_main_movies_table.sql'
path_to_sp_for_ETL='./admin/sql/sp_for_ETL.sql'
path_to_sp_for_get_movies='./admin/sql/sp_for_get_top_movies.sql'
path_to_delete_stg_db_script='./admin/sql/delete_stagingDB.sql'

path_to_ETL_movies_to_staging='./admin/ETL_movies_to_staging.py'
path_to_ETL_ratings_to_staging='./admin/ETL_ratings_to_staging.py'


mysql -u $1 -p$2 <<EOF
source $path_to_create_stg_db_script
use $staging_db_name
source $path_to_create_stg_movies_table_script
source $path_to_create_stg_ratings_table_script
EOF

python3 $path_to_ETL_movies_to_staging
python3 $path_to_ETL_ratings_to_staging

mysql -u $1 -p$2 <<EOF
source $path_to_create_main_db_script;
use $main_db_name;
source $path_to_create_main_movies_table_script;
source $path_to_sp_for_ETL;
call sp_for_ETL;
source $path_to_sp_for_get_movies;
source $path_to_delete_stg_db_script
EOF
