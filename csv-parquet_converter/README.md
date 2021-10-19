# Converter

Commandline app for convert data from .csv format to .parquet format or opposite. App can return schema or metadata .parquet file.

## Installation

Converter requires Python 3.7.1+ to run.   
Install the libraries:

```
pip install pyarrow
pip install pandas
```

## Usage

converter.py [-h] [-c2p | -p2c <src-filename> <dst-filename>] [-s <filename>] [-m <filename>] [-d <delimiter>]

## Apps arguments
```
-h, --help                                                                          show help message and exit  
-c2p <src-filename> <dst-filename>, --csv2parquet <src-filename> <dst-filename>     converts csv file to parquet file  
-p2c <src-filename> <dst-filename>, --parquet2csv <src-filename> <dst-filename>     converts parquet file to csv file  
-s <filename>, --get-schema <filename>                                              inputs the parquet file schema  
-m <filename>, --get-metadata <filename>                                            inputs the parquet file metadata  
-d <delimiter>, --delimiter <delimiter>                                             defines delimiter for csv file
```
