#! /bin/sh

Help()
{
    cat << EOF
usage: get_movies.sh [-h] [-s] [-n NUMBER] [-r REGEXP] [-f YEAR] [-t YEAR]
                     [-g "GENRE|GENRE|..."]

Commandline app for searching movies

optional arguments:
  -h, --help            show this help message and exit
  -s, --setupdb         download source movies file and setup/resetup databse
  -n NUMBER, --number NUMBER
                        the number of the best rated movies to output
  -r REGEXP, --regexp REGEXP
                        regular expression for searching by movie name
  -f YEAR, --year-from YEAR
                        sets the year for starting the search
  -t YEAR, --year-to YEAR
                        sets the year for finishing the search
  -g "GENRE|GENRE|...", --genres "GENRE|GENRE|..."
                        sets the genre/genres to search

EOF
}


Setupdb()
{
    if [ -d "data/" ]
    then
        rm -r data/
    fi
    mkdir data/
    echo 'Downloading data...'
    wget -O data/movies.zip -q https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
    unzip -q data/movies.zip ml-latest-small/movies.csv ml-latest-small/ratings.csv -d data/
    mv data/ml-latest-small/movies.csv data/
    mv data/ml-latest-small/ratings.csv data/
    echo
    echo 'Connecting to the database'
    read -p 'User: ' user
    stty -echo
    read -p 'Password: ' password
    stty echo
    echo ' '
    echo
    echo "Starting the database setup"
    sh ./admin/db_setup.sh $user $password
    echo "Ending the database setup"
    echo
    rm -r data/
}


Call_client()
{
    python3 ./admin/get_movies.py $number $regexp $year_from $year_to $genres
}


options=$(getopt -l "help,setupdb,number:,regexp:,year-from:,year-to:,genres:" -o "hsn:r:f:t:g:" -a -- "$@")
eval set -- "$options"
setupdb=0

while true
do
case $1 in
    -h|--help) 
        Help
        exit 0
        ;;
    -s|--setupdb)
        setupdb=1
        ;;
    -n|--number)
        shift
        number="-n "$1
        ;;
    -r|--regexp)
        shift
        regexp="-r "$1
        ;;
    -f|--year-from)
        shift
        year_from="-yf "$1
        ;;
    -t|--year-to)
        shift
        year_to="-yt "$1
        ;;
    -g|--genres)
        shift
        genres="-g "$1
        ;;
    --)
        shift
        break;;
esac
shift
done

if [ $setupdb = "1" ]
then
    Setupdb
    if [ "$number" ] || [ "$regexp" ] || [ "$year_from" ] || [ "$year_to" ] || [ "$genres" ]
    then 
        Call_client
    fi
else
    Call_client
fi
