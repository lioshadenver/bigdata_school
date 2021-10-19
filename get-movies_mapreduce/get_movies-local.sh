#! /bin/sh

Help()
{
    cat << EOF
usage: get_movies.sh [-h] [-s] [-n NUMBER] [-r REGEXP] [-f YEAR] [-t YEAR]
                     [-g "GENRE|GENRE|..."]

Commandline app for searching movies

optional arguments:
  -h, --help            show this help message and exit
  -d, --download_data         download source movies file
  -n NUMBER, --number NUMBER
                        the number movies to output
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


options=$(getopt -l "help,download-data,number:,regexp:,year-from:,year-to:,genres:" -o "hdn:r:f:t:g:" -a -- "$@")
eval set -- "$options"
download_data=0

while true
do
case $1 in
    -h|--help) 
        Help
        exit 0
        ;;
    -d|--download-data)
        download_data=1
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


download_data()
{
    if [ -d "data/" ]
    then
        rm -r data/
    fi
    mkdir data/
    echo 'Downloading data...'
    wget -O data/movies.zip -q https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
    unzip -q data/movies.zip ml-latest-small/movies.csv -d data/
    mv data/ml-latest-small/movies.csv data/
    rm -r data/movies.zip data/ml-latest-small
    echo 'MovieLens data downloaded successfully'
}


Executor()
{
    cat data/movies.csv |
    python3 mapper.py $regexp $year_from $year_to $genres |
    sort |
    python3 "reducer.py" $number |
    python3 finalizer.py
}


if [ $download_data = "1" ]
then
    download_data
    if [ "$number" ] || [ "$regexp" ] || [ "$year_from" ] || [ "$year_to" ] || [ "$genres" ]
    then 
        Executor
    fi
else
    Executor
fi
