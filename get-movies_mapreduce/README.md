# Get-movies

Command-line utility for searching and output the movies in csv format from the dataset

## Movies data

Utility use the [MovieLens dataset](https://grouplens.org/datasets/movielens/)

## Dependencies

For local script utility requires Python 3.6+ to run  
For hadoop script utility requires Apache Hadoop to run

## Usage

get_movies-local.sh [-h] [-d] [-n NUMBER] [-r REGEXP] [-f YEAR] [-t YEAR] [-g "GENRE|GENRE|..."]  
or
get_movies-hadoop.sh [-h] [-d] [-n NUMBER] [-r REGEXP] [-f YEAR] [-t YEAR] [-g "GENRE|GENRE|..."]

## Option
```
-h, --help                                          show this help message and exit  
-d, --download_data                                 download source movies file  
-n NUMBER, --number NUMBER                          the number movies to output  
-r REGEXP, --regexp REGEXP                          regular expression for searching by movie name  
-f YEAR, --year-from YEAR                           sets the year for starting the search  
-t YEAR, --year-to YEAR                             sets the year for finishing the search  
-g "GENRE|GENRE|...", --genres "GENRE|GENRE|..."    sets the genre/genres to search  
```

## Output

Local get_movies script output moveis in stdout, hadoop script save output in .txt file.

## Example

### Local script output in terminal:

```bash
$ sh get_movies-local.sh -n 3 -r way -f 2005 -g "comedy|drama"
Comedy;"Away We Go";2009
Comedy;"Castaway on the Moon (Kimssi pyoryugi)";2009
Comedy;"Flushed Away";2006
Drama;"Away from Her";2006
Drama;"Away We Go";2009
Drama;"Castaway on the Moon (Kimssi pyoryugi)";2009

$ sh get_movies-local.sh -n 5 -g crime
Comedy;"Away We Go";2009
Comedy;"Castaway on the Moon (Kimssi pyoryugi)";2009
Comedy;"Flushed Away";2006
Drama;"Away from Her";2006
Drama;"Away We Go";2009
Drama;"Castaway on the Moon (Kimssi pyoryugi)";2009
```

### Hadoop script output in file:
```bash
$ sh get_movies-hadoop.sh -n 2 -r "^L" -g "action|drama"
...
$ hdfs dfs -ls /final_output
Found 6 items
-rw-r--r--   1 lioshadenver hadoop          0 2021-08-31 21:38 /final_output/_SUCCESS
-rw-r--r--   1 lioshadenver hadoop         45 2021-08-31 21:38 /final_output/part-00000
-rw-r--r--   1 lioshadenver hadoop         61 2021-08-31 21:38 /final_output/part-00001
-rw-r--r--   1 lioshadenver hadoop          0 2021-08-31 21:38 /final_output/part-00002
-rw-r--r--   1 lioshadenver hadoop          0 2021-08-31 21:38 /final_output/part-00003

$ hdfs dfs -cat /final_output/part-00000
Drama;"Leal";2018
Drama;"Lovers Lost";1982

$ hdfs dfs -cat /final_output/part-00001
Action;"Legendary Amazons";2011
Action;"London Heist";2017
```