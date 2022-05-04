# floss - a financial data conversion tool

## Description
* Converts stock data from .csv and .txt files to json
* Default refresh rate is 1 second.

## Installation
 Place floss.py in the root folder of your project directory.

## Instructions
1. Run the program by specifying the input path and output path. (use -s to adjust speed)
2. Request data by writing a file path to chosen input file.
3. Retrieve retrieve data by reading from chosen output file.


## Usage
```bash
floss [-s speed] <input_path> <output_path>
```

## Examples
```bash
floss stock-data.csv output.json
```
```bash
floss -s 0.5 stock-data.csv output.json
```

##### CS361 Microservice

