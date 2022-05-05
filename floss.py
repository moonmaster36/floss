"""
Frank Vaughan
CS361: Software Engineering I
Assignment 7
"""

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
        self.output_path = None

    def argument_handler(self):
        """Returns arguments given from command line.

        Returns:
            stream_path: path to stream data-paths from
            output_path: path to write data to
        """
        parser = argparse.ArgumentParser(prog="floss",
                                         description="Converts stock data from text and csv files to json",
                                         usage="py %(prog)s.py [options] input_path output_path")
        parser.add_argument("-s", "--speed", help="Changes how quickly the stream_path is re-checked.",
                            type=float, action='store', default=1)
        parser.add_argument(
            "input_path", help="Text file containing path to data", type=str)
        parser.add_argument(
            "output_path", help="JSON file to write data to", type=str)

        args = parser.parse_args()

        if args.speed < 0:
            print(f'speed cannot be negative')

        self.speed = args.speed
        print(f'speed = {self.speed}')

        stream_path = args.input_path
        output_path = args.output_path
        self.stream_path = output_path
        self.output_path = output_path

        return stream_path, output_path

    @staticmethod
    def get_txt_data(txt_file):
        """Fetches data from .txt file

        Args:
            txt_file (.txt): file containing data

        Returns:
            list: list of dictionaries
        """
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
        """Converts data from .txt source to json then writes data to output_path.

        Args:
            data (list): stock data
            output_path (.json file): path to output file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

            # Get last part of path for cleaner printing.
            # cur_path = os.path.basename(os.path.normpath(txt_file))
            file_path = pathlib.PurePath(output_path)

            print(f'floss wrote data to {file_path}')

    @staticmethod
    def get_csv_data(path):
        """Fetches data from .csv file and converts the data
            into a list .

        Args:
            path (.csv): path to csv data

        Returns:
            list of dictionaries, each dictionary is a row from csv data
        """
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
            return data

    def csv_service(self, csv_path, output_path):
        """Extracts data from .csv file and writes it to the
            specified output file in JSON format.

        Args:
            csv_path (.csv): source of data
            output_path (.json): file to write data to
        """
        data = self.get_csv_data(csv_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

            # Get last part of path for cleaner printing.
            file_path = pathlib.PurePath(output_path)
            print(f'floss wrote data from {csv_path} to {file_path}')

    @staticmethod
    def validate_arguments(stream_path, output_path):
        """Validates file paths given as arguments.

        Args:
            stream_path (.txt): file to read data paths from
            output_path (.json): file to write data to

        Returns:
            bool: True if paths are valid, false if not
        """        
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
            print(
                f'Invalid stream file type {stream_type}, streams must be .txt files.')
            return False

        if output_type != '.json':
            print(
                f'Invalid output file type {output_type}, output must be a .json file.')
            return False

        return True

    def file_service(self, input_path, output_path):
        """Reads paths from stream file, then converts
            the .txt or .csv file into json data.

        Args:
            input_path (.txt or .csv): path to data
            output_path (.json): path to output file

        Returns:
            _type_: True if data was written, False if not.
        """
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

    def read_file_stream(self, stream_path):
        """Core loop of program.
            Reads data path files, fetches data, writes data to output.

        Args:
            stream_path (.txt): input file to read data paths from
        """
        # Wait for changes in input file.
        last_size = 0
        last_path = ''
        run = True

        while run:
            # On change, copy contents of input file. Write contents to given output JSON file.
            file_size = os.path.getsize(stream_path)
            output_size = os.path.getsize(self.output_path)

            if file_size > 0 and output_size == 0:
                # Attempt to read the path input from stream file
                with open(stream_path, "r") as f:
                    data_path = f.readline()
                    if data_path != last_path:  # If this is a new path, fetch data.
                        # Track the last stock_path entered
                        last_size = file_size
                        last_path = data_path
                        result = self.file_service(
                            data_path, self.output_path)
                        run = result

            time.sleep(self.speed)

        print(f'\nStream stopped.')

    def main_loop(self):       
        """Calls all functions needed to operate program.

        Returns:
            int: 0 if program exited successfuly, else 1
        """
        
        # get args
        stream_path, output_path = self.argument_handler()
        # stream_path = 'stream.txt'
        # output_path = 'output.json'
        print(f'Reading data file paths from {stream_path}')
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
        self.read_file_stream(stream_path)
        sys.exit(0)

if __name__ == '__main__':
    floss = Floss()
    floss.main_loop()
