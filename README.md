# floss
CS 361 Assignment 7 Micro-Service

Description:
    * Converts stock data from text and csv files to json 
    * Reads file paths from given input file.
    * Input file only accepts .txt or .csv files
    * Speed is optional. Default value is 1.
Parameters:
    - input_path: Text file containing path to data
    - output_path: JSON file to write data to
    - speed: speed at which program checks input file for new path

Instructions:
   1. Place floss.py in the root folder of your project directory.
   2. Start the program.
   3. Request data by writing a file path to chosen input file.
   4. Retrieve retrieve data by reading from chosen output file.

Example Usage: 
     floss --speed 2 input.txt output-file.json
     floss -s 2 input.txt output-file.json 

