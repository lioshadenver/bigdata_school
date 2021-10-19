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
    hdfs dfs -test -d "/data"
    if [ $? -eq 0 ] 
    then
        hdfs dfs -rm -r /data/
    fi
    hdfs dfs -mkdir /data/
    echo 'Downloading data...'
    wget -O /tmp/movies.zip -q https://files.grouplens.org/datasets/movielens/ml-latest-small.zip
    unzip -q /tmp/movies.zip ml-latest-small/movies.csv -d /tmp
    hdfs dfs -put /tmp/ml-latest-small/movies.csv /data/
    rm -d -r /tmp/movies.zip /tmp/ml-latest-small
    echo 'MovieLens data downloaded successfully'
}


Executor()
{
    hdfs dfs -rm -r /output
    hdfs dfs -rm -r /final_output

    yarn jar /usr/lib/hadoop/hadoop-streaming.jar \
        -input /data/movies.csv \
        -output /output \
        -file mapper.py reducer.py \
        -mapper "python3 mapper.py $regexp $year_from $year_to $genres" \
        -reducer "python3 reducer.py $number"

    yarn jar /usr/lib/hadoop/hadoop-streaming.jar \
        -D mapred.map.tasks=3 \
        -D mapred.reduce.tasks=0 \
        -input /output \
        -output /final_output \
        -file finalizer.py \
        -mapper "python3 finalizer.py"
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
