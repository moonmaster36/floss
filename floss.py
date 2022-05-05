"""
Frank Vaughan
CS361: Software Engineering I
Assignment 7
g"""

import time
import os
import pathlib
import sys
import argparse
import json
import csv


class Floss:
    def __init__(self):
        self.speed = None
        self.stream_path = None
        self.input_path = None
        self.output_path = None

    def argument_handler(self):
        """
        * Returns arguments given from command line.
        * Arguments:
        *   stream_path: path to stream data-paths from.
        *   json_file: path to write data to.
        * Both arguments are required.
        * Allows users to get help by adding modifier -help
        """
        parser = argparse.ArgumentParser(prog="floss",
                                         description="Converts stock data from text and csv files to json",
                                         usage="%(prog)s [options] input_path output_path")
        parser.add_argument("-s", "--speed", help="Changes how quickly the stream_path is re-checked.",
                            type=float, action='store', default=1)
        parser.add_argument("input_path", help="Text file containing path to data", type=str)
        parser.add_argument("output_path", help="JSON file to write data to", type=str)

        args = parser.parse_args()

        if args.speed < 0:
            print(f'speed cannot be negative')

        self.speed = args.speed
        print(f'speed = {self.speed}')
        stream_path = args.input_path
        output_path = args.output_path

        return stream_path, output_path

    @staticmethod
    def get_txt_data(txt_file):
        """Handles retrieval of data from .txt files."""
        if not os.path.isfile(txt_file):
            print('File does not exist.')
            return

        with open(txt_file, 'r') as reader:
            stocks = []

            for line in reader:
                cur = {}
                company = ''
                ticker = ''

                x = 0
                while line[x] != ':':
                    company += line[x]
                    x += 1
                x += 1
                for i in range(x, len(line) - 1):
                    ticker += line[i]

                cur['name'] = company
                cur['ticker'] = ticker

                stocks.append(cur)

            return {'data': stocks}

    @staticmethod
    def txt_service(data, output_path):
        """
        * Handles .txt input files.
        * Retrieves data from file specified in txt_file, converts data to JSON,
            then writes data to file specified in json_file.

        :param data: stock data to write to file.
        :param output_path: file to write json data to
        :return: None
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

            # Get last part of path for cleaner printing.
            # cur_path = os.path.basename(os.path.normpath(txt_file))
            file_path = pathlib.PurePath(output_path)

            print(f'floss wrote data to {file_path}')

    @staticmethod
    def get_csv_data(path):
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
            return data

    def csv_service(self, csv_path, output_path):
        """
        * Extracts data from .csv file and writes it to the
            specified output in JSON format.
        * csvfile: path to .cvs file containing data.
        * json_file: path to .json file to write data.
        """
        data = self.get_csv_data(csv_path)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

            # Get last part of path for cleaner printing.
            # cur_path = os.path.basename(os.path.normpath(txt_file))
            file_path = pathlib.PurePath(output_path)
            print(f'floss wrote data to {file_path}')

    @staticmethod
    def validate_arguments(stream_path, output_path):
        # Check if stream path exists
        if not os.path.isfile(stream_path):
            print('Stream file not found.')
            return False

        # Check if output path exists
        if not os.path.isfile(output_path):
            print('Output file not found.')
            return False
        # Extract stream/output file type.
        stream_type = os.path.splitext(stream_path)[1]
        output_type = os.path.splitext(output_path)[1]

        # Validate stream/output file types.
        if stream_type != '.txt':
            print(f'Invalid stream file type {stream_type}, streams must be .txt files.')
            return False

        if output_type != '.json':
            print(f'Invalid output file type {output_type}, output must be a .json file.')
            return False

        return True

    def file_service(self, input_path, output_path):
        # Check if input path exists
        if not os.path.isfile(input_path):
            print('Input file not found.')
            return False

        # Check if output path exists
        if not os.path.isfile(output_path):
            print('Output file not found.')
            return False

        # Extract input/output file type.
        input_type = os.path.splitext(input_path)[1]
        output_type = os.path.splitext(output_path)[1]

        if input_type == '.txt':
            data = self.get_txt_data(input_path)
            try:
                self.txt_service(data, output_path)
            except Exception as err:
                print(f'Unexpected error opening {input_path} is', repr(err))
                return False

        elif input_type == '.csv':
            try:
                self.csv_service(input_path, output_path)
            except Exception as err:
                print(f'Unexpected error opening {input_path} is', repr(err))
                return False

        elif output_type != '.json':
            print(f'Unsupported input file type: {input_type}')
            return False
        else:
            print(f'Unsupported input file type: {input_type}')
            return False

        return True

    def read_file_stream(self, stream_path, output_path):
        """Main loop of program."""
        # Wait for changes in input file.
        last_size = 0
        run = True
        while run:
            # Attempt to read the path input from stream file
            with open(stream_path, "r") as f:
                data_path = f.readline()
            time.sleep(self.speed)

            # On change, copy contents of input file. Write contents to given output JSON file.
            file_size = os.path.getsize(stream_path)
            output_size = os.path.getsize(output_path)
            if file_size != last_size and output_size == 0:
                print(f'data_path: {data_path}')
                # Track the last stock_path entered
                last_size = file_size

                result = self.file_service(data_path, output_path)
                run = result
            else:
                print('Waiting for space in output.')
        print(f'\nStream stopped.')

    def main_loop(self):
        # get args
        stream_path, output_path = self.argument_handler()
        # stream_path = 'stream.txt'
        # output_path = 'output.json'
        print(F'stream_path: {stream_path}')
        print(F'output_path: {output_path}\n')

        # Validate args.
        if not self.validate_arguments(stream_path, output_path):
            return 'Invalid args'

        # Check if output_path is empty.
        if os.path.getsize(output_path) > 0:
            # Ask user if they want to rewrite the output_path, or exit.
            text = input(f"{output_path} is not empty. Overwrite? y/n ")
            text = text.lower()
            if len(text) > 1:
                print("Invalid response. Exiting floss.")
                sys.exit(1)
            if text == 'y':
                # Erase contents of output_path
                open(output_path, 'w').close()
            else:
                # Exit
                print("Exiting floss.")
                sys.exit(1)

        # Read from stream file for input paths.
        self.read_file_stream(stream_path, output_path)


if __name__ == '__main__':
    floss = Floss()
    floss.main_loop()
