import os
import pandas as pd
import requests
import json
from tqdm import tqdm
from datetime import datetime

class Processor:
    def __init__(self, output_dir="nasa_power_data", database_file="district_database.csv",
                 merged_file="merged_all_districts.csv", params_file=None,
                 log_file="logs/processor.log"):
        self.output_dir = output_dir
        self.database_file = database_file
        self.merged_file = merged_file
        self.base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        self.df_database = pd.read_csv(database_file)

        # Setup log file
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Default API parameters
        self.default_params = {
            "start": "20040101",  # YYYYMMDD
            "end": "20240801",
            "community": "ag",
            "parameters": ",".join([
                "ALLSKY_SFC_SW_DWN", "CLRSKY_SFC_SW_DWN", "ALLSKY_SFC_PAR_TOT", "ALLSKY_SFC_UV_INDEX",
                "T2M", "T2MDEW", "TS", "T2M_RANGE", "QV2M", "RH2M", "PRECTOTCORR",
                "PS", "WS2M", "WD2M", "GWETTOP", "GWETROOT", "GWETPROF"
            ]),
            "format": "csv",
            "header": "false"
        }

        # Load parameters
        self.params = self.load_params(params_file) if params_file else self.default_params.copy()

        self.log("Processor initialized.")

    def log(self, message):
        """Append a log message with timestamp to the logfile."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp}    {message}\n")

    def load_params(self, params_file):
        if not os.path.exists(params_file):
            raise FileNotFoundError(f"JSON file {params_file} not found.")
        with open(params_file, 'r') as file:
            params = json.load(file)
        self.log(f"Loaded parameters from {params_file}")
        return params

    def save_params(self, output_file="saved_params.json"):
        """Save current parameters to a JSON file."""
        with open(output_file, 'w') as f:
            json.dump(self.params, f, indent=4)
        self.log(f"Parameters saved to {output_file}")

    def edit_default_params(self, **kwargs):
        """Edit default parameters dynamically."""
        for key, value in kwargs.items():
            if key in self.default_params:
                self.default_params[key] = value
                self.params[key] = value  # Also update current parameters
                self.log(f"Updated default param: {key} = {value}")
            else:
                self.log(f"Warning: '{key}' is not a recognized parameter key.")

    def merge_csv_files(self):
        all_dataframes = []
        csv_files = [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir) if f.endswith(".csv")]

        self.log("Merging CSV files started.")
        for file in tqdm(csv_files, desc="Merging CSVs"):
            df = pd.read_csv(file)
            all_dataframes.append(df)

        if all_dataframes:
            merged_df = pd.concat(all_dataframes, ignore_index=True)
            merged_df.to_csv(self.merged_file, index=False)
            self.log(f"Merged CSV saved as {self.merged_file}")
        else:
            self.log("No CSV files found to merge.")

    def add_location_data(self):
        self.log("Started adding location data to CSVs.")
        for file in tqdm(os.listdir(self.output_dir), desc="Adding location data"):
            if file.endswith(".csv"):
                region_name = file.replace(".csv", "")
                region_info = self.df_database[self.df_database["Region"] == region_name]

                if region_info.empty:
                    self.log(f"No matching region found for {region_name}")
                    continue

                lat, lon = region_info.iloc[0]["Latitude"], region_info.iloc[0]["Longitude"]
                file_path = os.path.join(self.output_dir, file)
                df = pd.read_csv(file_path)

                df.insert(0, "Region", region_name)
                df.insert(1, "Latitude", lat)
                df.insert(2, "Longitude", lon)
                df.to_csv(file_path, index=False)
                self.log(f"Added location info to {file_path}")

    def download_nasa_data(self, region, lat, lon):
        params = self.params.copy()
        params["latitude"] = lat
        params["longitude"] = lon
        self.log(f"Starting download for {region} ({lat}, {lon})")

        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                filename = os.path.join(self.output_dir, f"{region}.csv")
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(response.text)
                self.log(f"Downloaded and saved data for {region} → {filename}")
                return True
            else:
                self.log(f"Failed to download data for {region} - Status Code: {response.status_code}")
                return False
        except Exception as e:
            self.log(f"Error downloading {region}: {str(e)}")
            return False

    def download_data_for_all_districts(self):
        self.log("Started downloading NASA data for all regions.")
        success_count = 0
        for _, row in tqdm(self.df_database.iterrows(), total=len(self.df_database), desc="Downloading NASA data"):
            if self.download_nasa_data(row["Region"], row["Latitude"], row["Longitude"]):
                success_count += 1
        self.log(f"Downloaded data for {success_count}/{len(self.df_database)} regions")

    def clean_csv_files(self):
        self.log("Started cleaning CSV files (removing first 25 rows).")
        for file in tqdm(os.listdir(self.output_dir), desc="Cleaning CSV files"):
            if file.endswith(".csv"):
                file_path = os.path.join(self.output_dir, file)
                try:
                    df = pd.read_csv(file_path, skiprows=25)
                    df.to_csv(file_path, index=False)
                    self.log(f"Cleaned and saved: {file_path}")
                except Exception as e:
                    self.log(f"Error cleaning {file_path}: {str(e)}")

