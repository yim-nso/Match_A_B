# CSV Comparison Tool Documentation

## Overview
The CSV Comparison Tool is designed to compare two CSV files using a sophisticated 3-stage matching process implemented with the powerful data manipulation libraries, **Pandas** and **Polars**.

## Features
- **3-Stage Matching**: This tool processes CSV file comparisons in three distinct stages to ensure accurate results.
- **Use of Pandas and Polars**: Leverage the capabilities of both libraries for efficient data handling and manipulation.

## Stage 1: Data Loading 
In the first stage, the tool loads the CSV files into dataframes using either Pandas or Polars, facilitating a smooth comparison process.

## Stage 2: Data Cleaning 
This stage involves cleaning and preprocessing the data to ensure uniformity and remove any discrepancies before comparison.

## Stage 3: Data Comparison 
The final stage compares the two cleaned datasets and highlights the differences, producing a comprehensive report of the discrepancies.

## Installation
To use the CSV Comparison Tool, ensure you have the required libraries installed:
```
pip install pandas polars
```  

## Usage
To use the tool, simply call the function defined within the script, passing the file paths of the two CSVs you wish to compare.

## Conclusion
This CSV Comparison Tool is an essential utility for data analysis, enabling quick and efficient comparisons of CSV files to identify differences and similarities through a reliable three-stage process.