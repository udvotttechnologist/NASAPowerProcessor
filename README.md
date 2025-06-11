# NASA Power Data Processor - README

## Overview
This Python library provides a convenient way to download and process climate data from NASA's POWER (Prediction Of Worldwide Energy Resource) API for multiple geographic regions. The processor handles data downloading, cleaning, merging, and adding location metadata automatically.

## Installation

### Prerequisites
- Python 3.6 or higher
- Required Python packages (install with `pip install -r requirements.txt`)

### Required Packages
```
pandas>=1.0.0
requests>=2.25.0
tqdm>=4.50.0
```

You can install all requirements with:
```bash
pip install pandas requests tqdm
```

## Usage Instructions

### 1. Prepare Your District Database
Create a CSV file containing the regions you want to download data for. The file must include these columns:
- `Region`: Name of the region/district (will be used in filenames)
- `Latitude`: Decimal latitude coordinate
- `Longitude`: Decimal longitude coordinate

Example `district_database.csv`:
```
Region,Latitude,Longitude
New_York,40.7128,-74.0060
London,51.5074,-0.1278
Tokyo,35.6762,139.6503
```

### 2. Initialize the Processor
```python
from NASADataProcessor import Processor

# Basic initialization
processor = Processor(
    output_dir="nasa_data",          # Where to save downloaded files
    database_file="districts.csv",   # Your district database file
    merged_file="all_data.csv",      # Final merged output filename
    log_file="logs/processor.log"    # Log file path
)
```

### 3. (Optional) Customize API Parameters
You can modify the default parameters either by:
- Editing the default parameters in code
- Loading from a JSON file

#### Option A: Edit parameters programmatically
```python
processor.edit_default_params(
    start="20100101",       # New start date (YYYYMMDD)
    end="20201231",         # New end date
    parameters="T2M,RH2M"   # Only request temperature and humidity
)
```

#### Option B: Load from JSON file
Create a `params.json` file:
```json
{
    "start": "20150101",
    "end": "20201231",
    "community": "ag",
    "parameters": "T2M,RH2M,PRECTOTCORR",
    "format": "csv",
    "header": "false"
}
```
Then initialize with:
```python
processor = Processor(params_file="params.json")
```

### 4. Download Data
Download data for all regions in your database:
```python
processor.download_data_for_all_districts()
```

This will:
1. Create individual CSV files for each region in your output directory
2. Show a progress bar
3. Log all activities

### 5. Clean Downloaded Files
NASA POWER CSVs have 25 header rows that need to be removed:
```python
processor.clean_csv_files()
```

### 6. Add Location Metadata
Add region names and coordinates to each CSV:
```python
processor.add_location_data()
```

### 7. Merge All Files
Combine all individual CSVs into one master file:
```python
processor.merge_csv_files()
```

## Complete Workflow Example
```python
from NASADataProcessor import Processor

# Initialize with custom parameters
processor = Processor(
    output_dir="climate_data",
    database_file="my_districts.csv",
    merged_file="combined_climate_data.csv"
)

# Download data for all regions
processor.download_data_for_all_districts()

# Process the files
processor.clean_csv_files()
processor.add_location_data()
processor.merge_csv_files()

print("Data processing complete!")
```

## Default Parameters
The processor comes with these default parameters:
- Start Date: 2004-01-01
- End Date: 2024-08-01
- Community: "ag" (agriculture)
- Parameters: Includes 17 climate variables (solar radiation, temperature, precipitation, etc.)
- Format: CSV
- Header: false

## Output Files
- Individual region files: `[output_dir]/[Region].csv`
- Merged file: `[merged_file]`
- Log file: `[log_file]`

## Error Handling
- The processor logs all activities and errors
- Failed downloads will be logged but won't stop the process
- Check the log file for troubleshooting

## Tips
1. Start with a small test dataset (2-3 regions) to verify your setup
2. Monitor the log file (`processor.log`) for progress and errors
3. The API has rate limits - very large datasets may need to be downloaded in batches
4. You can resume interrupted downloads - the processor won't re-download existing files

## NASA POWER API Reference
For more information about available parameters and data:
https://power.larc.nasa.gov/docs/services/api/

## License
This project is open source under the MIT License.

## Citation Requirement

All public uses (publications, presentations, derivatives) **must include attribution** using one of these formats:

### BibLaTeX (Recommended for Academic Work)
```bibtex
@software{NASA_Power_Processor,
  author       = {Paul, Tonmoy},
  title        = {NASA Power Data Processor},
  year         = {2025},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  howpublished = {\url{https://github.com/udvotttechnologist/NASAPowerProcessor.git}},
  version      = {1.0},
  license      = {MIT License}
}
```
