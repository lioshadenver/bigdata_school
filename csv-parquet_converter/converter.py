#!/usr/bin/env python3
from argparse import ArgumentParser
from pyarrow import csv
import pyarrow.parquet as pq


def main():
    args = get_args()
    if args.csv2parquet:
        convert_csv2parquet(args.csv2parquet[0], args.csv2parquet[1], args.delimiter)
    if args.parquet2csv:
        convert_parquet2csv(args.parquet2csv[0], args.parquet2csv[1], args.delimiter)
    if args.get_schema:
        schema = get_schema(args.get_schema[0])
        if schema:
            print(schema)
    if args.get_metadata:
        metadata = get_metadata(args.get_metadata[0])
        if metadata:
            print(metadata)


def get_args():
    '''
    function parses arguments from terminal
    '''
    parser = ArgumentParser(description='Commandline app for convert data from csv format to parquet format or opposite')
    parser.add_argument(
        '-c2p','--csv2parquet',
        nargs=2,
        metavar=('<src-filename>', '<dst-filename>'),
        help='converts csv file to parquet file')
    parser.add_argument(
        '-p2c', '--parquet2csv',
        nargs=2,
        metavar=('<src-filename>', '<dst-filename>'),
        help='converts parquet file to csv file')
    parser.add_argument(
        '-s', '--get-schema',
        nargs=1,
        metavar='<filename>',
        help='outputs the parquet file schema')
    parser.add_argument(
        '-m', '--get-metadata',
        nargs=1,
        metavar='<filename>',
        help='outputs the parquet file metadata')
    parser.add_argument(
        '-d', '--delimiter',
        default=',',
        metavar='<delimiter>',
        help='defines delimiter for csv file')
    return parser.parse_args()


def convert_csv2parquet(src_path, dst_path, delimiter):
    '''
    converts data from .csv format to .parquet format
    '''
    try:
        parse_opt = csv.ParseOptions(delimiter=delimiter)
        table = csv.read_csv(src_path, parse_options=parse_opt)
        with pq.ParquetWriter(dst_path, table.schema) as writer:
            writer.write_table(table, row_group_size=None)
        print(f'file successfully convert to {dst_path}')
    except Exception as err:
        print(f'error when converting csv to parquet: {err}')
        

def convert_parquet2csv(src_path, dst_path, delimiter):
    '''
    converts data from .parquet format to .csv format
    '''
    try:
        table = pq.read_table(src_path)
        table.to_pandas().to_csv(dst_path, sep=delimiter, index=False)
        print(f'file successfully convert to {dst_path}')
    except Exception as err:
        print(f'error when converting parquet to csv: {err}')


def get_schema(path):
    '''
    returns parquet file schema
    '''
    try:
        schema = str(pq.read_table(path)).splitlines()[1:]
        return '\n'.join(schema)
    except Exception as err:
        print(f'error when get schema: {err}')


def get_metadata(path):
    '''
    returns parquet file metadata
    '''
    try:
        parquet_file = pq.ParquetFile(path)
        metadata = str(parquet_file.metadata).splitlines()[1:]
        return '\n'.join(metadata)
    except Exception as err:
        print(f'error when get metadata: {err}')


if __name__ == '__main__':
    main()
