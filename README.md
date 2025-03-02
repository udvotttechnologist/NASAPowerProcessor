# `NASADataProcessor` Python Package Documentation

The `NASADataProcessor` package is designed to help you process and download data from NASA's POWER API, handle district-specific data, merge CSV files, and manage latitude/longitude information. The package uses Object-Oriented Programming (OOP) to provide a modular, reusable, and maintainable interface for handling NASA's Power data.

## Table of Contents

1. [Class Overview](#class-overview)
2. [Methods](#methods)
    - [__init__](#init)
    - [load_params](#load_params)
    - [merge_csv_files](#merge_csv_files)
    - [add_location_data](#add_location_data)
    - [download_nasa_data](#download_nasa_data)
    - [download_data_for_all_districts](#download_data_for_all_districts)
    - [clean_csv_files](#clean_csv_files)
3. [Usage Examples](#usage-examples)
4. [Configuration](#configuration)
    - [Default Parameters](#default-parameters)
    - [Custom Parameters File](#custom-parameters-file)
5. [Error Handling](#error-handling)
6. [Requirements](#requirements)

---

## Class Overview

The `NASADataProcessor` class allows you to interact with NASA's POWER API, process the data, and handle various tasks like merging CSV files, adding district-specific information, downloading data for all districts, and cleaning CSV files.

### Methods

#### `__init__(self, output_dir="nasa_power_data", database_file="district_database.csv", merged_file="merged_all_districts.csv", params_file=None)`

The constructor initializes the class with necessary paths, database, and parameters.

##### Parameters:
- `output_dir` (str): Directory to store the downloaded CSV files. Default is `"nasa_power_data"`.
- `database_file` (str): Path to the district database CSV file. Default is `"district_database.csv"`.
- `merged_file` (str): Name of the merged CSV file. Default is `"merged_all_districts.csv"`.
- `params_file` (str, optional): Path to a custom JSON file containing API parameters. If not provided, default parameters will be used.

##### Example Usage:
```python
processor = Processor(output_dir="data", database_file="district_db.csv", params_file="custom_params.json")
```

---

#### `load_params(self, params_file)`

This method loads API parameters from a specified JSON file.

##### Parameters:
- `params_file` (str): Path to the JSON file containing API parameters.

##### Returns:
- A dictionary containing the parameters from the JSON file.

##### Raises:
- `FileNotFoundError`: If the JSON file is not found.

##### Example Usage:
```python
params = processor.load_params("custom_params.json")
```

---

#### `merge_csv_files(self)`

Merges all CSV files in the output directory into a single CSV file.

##### Example Usage:
```python
processor.merge_csv_files()
```

---

#### `add_location_data(self)`

Adds location data (latitude, longitude) and district information to each CSV file in the output directory.

##### Example Usage:
```python
processor.add_location_data()
```

---

#### `download_nasa_data(self, district, lat, lon)`

Downloads data for a specific district using NASA's POWER API and saves the data as a CSV file.

##### Parameters:
- `district` (str): Name of the district.
- `lat` (float): Latitude of the district.
- `lon` (float): Longitude of the district.

##### Example Usage:
```python
processor.download_nasa_data("DistrictA", 23.8103, 90.4125)
```

---

#### `download_data_for_all_districts(self)`

Downloads data for all districts listed in the district database file.

##### Example Usage:
```python
processor.download_data_for_all_districts()
```

---

#### `clean_csv_files(self)`

Removes the first 25 rows from each CSV file in the output directory.

##### Example Usage:
```python
processor.clean_csv_files()
```

---

## Usage Examples

Here is how you can use the `NASADataProcessor` class:

### Example 1: Initialize and Merge CSV Files

```python
# Initialize the processor with default parameters
processor = NASADataProcessor()

# Merge all CSV files into one
processor.merge_csv_files()
```

### Example 2: Add Location Data

```python
# Initialize the processor
processor = NASADataProcessor()

# Add latitude, longitude, and district information to each CSV file
processor.add_location_data()
```

### Example 3: Download Data for a Single District

```python
# Initialize the processor
processor = NASADataProcessor()

# Download data for a specific district
processor.download_nasa_data("DistrictA", 23.8103, 90.4125)
```

### Example 4: Download Data for All Districts

```python
# Initialize the processor
processor = NASADataProcessor()

# Download data for all districts from the database
processor.download_data_for_all_districts()
```

### Example 5: Clean CSV Files

```python
# Initialize the processor
processor = NASADataProcessor()

# Clean all CSV files by removing the first 25 rows
processor.clean_csv_files()
```

---

## Configuration

### Default Parameters

If no custom parameters are provided, the default parameters are as follows:

```json
{
  "start": "20040101",
  "end": "20240801",
  "community": "ag",
  "parameters": "ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,ALLSKY_SFC_PAR_TOT,ALLSKY_SFC_UV_INDEX,T2M,T2MDEW,TS,T2M_RANGE,QV2M,RH2M,PRECTOTCORR,PS,WS2M,WD2M,GWETTOP,GWETROOT,GWETPROF",
  "format": "csv",
  "header": "true"
}
```

These default parameters can be modified by specifying a custom JSON file.

### Custom Parameters File

To use custom parameters, create a JSON file (e.g., `custom_params.json`) with the desired parameters. Example of a JSON file:

```json
{
  "start": "20080101",
  "end": "20230801",
  "community": "ag",
  "parameters": "T2M,T2MDEW,TS",
  "format": "csv",
  "header": "true"
}
```

Pass this file to the `NASADataProcessor` constructor:

```python
processor = NASADataProcessor(params_file="custom_params.json")
```

---

## Error Handling

- **FileNotFoundError**: Raised if the custom parameters file is not found.
- **requests.exceptions.RequestException**: This is raised if there is an issue with the HTTP request to the NASA POWER API.
- **FileNotFoundError**: If the district database or any required file is missing, an error message will be displayed.
  
The package handles missing files gracefully and prints appropriate error messages to guide the user.

---

## Requirements

- Python 3.6+
- Required libraries:
  - `pandas`
  - `requests`
  - `json` (standard library)

Install the required libraries using `pip`:

```bash
pip install pandas requests
```

---

This documentation provides a comprehensive guide to using the `NASADataProcessor` class for interacting with NASA's POWER API and processing district data efficiently.

