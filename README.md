# floss
CS 361 Assignment 7 Micro-Service

* Description:
    * Converts stock data from text and csv files to json 
    * Reads file paths from given input file.
    * Input file only accepts .txt or .csv files
    * Speed is optional. Default value is 1.

Instructions:
* Request data by writing file path to input file. 

* Parameters:
    - input_path: Text file containing path to data
    - output_path: JSON file to write data to
    - speed: speed at which program checks input file for new path

* Example Usage: 
     floss --speed 2 input.txt output-file.json
     floss -s 2 input.txt output-file.json 

