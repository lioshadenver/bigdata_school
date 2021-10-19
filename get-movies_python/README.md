# Get-movies

Command-line utility for searching and output the most rated movies in csv format from the dataset

## Movies data

Utility use the [MovieLens dataset](https://grouplens.org/datasets/movielens/)

## Dependencies

Utility requires Python 3.6+ to run

## Usage

get_movies.py [-h] [-n NUMBER] [-r REGEXP] [-yf YEAR] [-yt YEAR] [-g "GENRE|GENRE|..."]

## Option
```
-h, --help                                          show this help message and exit  
-n NUMBER, --number NUMBER                          the number of the best rated movies to output  
-r REGEXP, --regexp REGEXP                          regular expression for searching by movie name  
-yf YEAR, --year-from YEAR                          sets the year for starting the search  
-yt YEAR, --year-to YEAR                            sets the year for finishing the search  
-g "GENRE|GENRE|...", --genres "GENRE|GENRE|..."    sets the genre/genres to search  
```

## Example

```bash
$ python3 get_movies.py -n 3 -r way -yf 2005 -g "comedy|drama"
Comedy,"Castaway on the Moon (Kimssi pyoryugi)",2009,4.0
Comedy,"Oh, Hello: On Broadway",2017,3.5
Comedy,"Away We Go",2009,3.5
Drama,"Castaway on the Moon (Kimssi pyoryugi)",2009,4.0
Drama,"Away from Her",2006,3.6
Drama,"Runaways, The",2010,3.5
```
```bash
$ python3 get_movies.py -n 5 -g crime
Crime,"Loving Vincent",2017,5.0
Crime,"L.A. Slasher",2015,5.0
Crime,"Tokyo Tribe",2014,5.0
Crime,"Hunting Elephants",2013,5.0
Crime,"On the Other Side of the Tracks (De l'autre côté du périph)",2012,5.0
```
