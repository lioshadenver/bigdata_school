# Get-movies

Command-line utility for searching and output the most rated movies in csv format from the dataset

## Movies data

Utility use the [MovieLens dataset](https://grouplens.org/datasets/movielens/)

## Dependencies

Utility requires Python 3.6+, MySQL Community Server 8.0.26+, Connector/Python 8.0.26+ to run

## Usage

get_movies.sh [-h] [-s] [-n NUMBER] [-r REGEXP] [-f YEAR] [-t YEAR] [-g "GENRE|GENRE|..."]

## Option
```
-h, --help                                          show this help message and exit  
-s, --setupdb                                       download source movies file and setup/resetup databse  
-n NUMBER, --number NUMBER                          the number of the best rated movies to output  
-r REGEXP, --regexp REGEXP                          regular expression for searching by movie name  
-f YEAR, --year-from YEAR                           sets the year for starting the search  
-t YEAR, --year-to YEAR                             sets the year for finishing the search  
-g "GENRE|GENRE|...", --genres "GENRE|GENRE|..."    sets the genre/genres to search  
```

## Example

```bash
$ sh get_movies.sh -n 3 -r way -f 2005 -g "comedy|drama"
Comedy,"Bill Burr: I'm Sorry You Feel That Way",2014,4.5
Comedy,"Bill Burr: Walk Your Way Out",2017,4.0
Comedy,"Castaway on the Moon (Kimssi pyoryugi)",2009,4.0
Drama,"Way Back, The",2010,4.0
Drama,"Castaway on the Moon (Kimssi pyoryugi)",2009,4.0
Drama,"Away from Her",2006,3.6
```
```bash
$ sh get_movies.sh -n 5 -g crime
Crime,"Loving Vincent",2017,5.0
Crime,"L.A. Slasher",2015,5.0
Crime,"Tokyo Tribe",2014,5.0
Crime,"Hunting Elephants",2013,5.0
Crime,"On the Other Side of the Tracks (De l'autre côté du périph)",2012,5.0
```
