# floss - a financial data conversion tool
* Converts stock data from .csv and .txt files to json
* Default refresh rate is 1 second.

## Installation
 Place floss.py in the root folder of your project directory.

## Instructions
1. Run the program by specifying the input path and output path. (use -s to adjust refresh rate)
3. Request data by writing a file path to chosen input file.
4. Retrieve data by reading from chosen output file.


## Usage
```bash
python floss.py [-s speed] <input_path> <output_path>
```

## Example Usage
To use the default program speed.
```bash
python floss stock-data.csv output.json
```
To change the program speed.
```bash
python floss -s 0.5 stock-data.csv output.json
```
