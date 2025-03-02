import os
import pandas as pd
import requests
import json

class Processor:
    def __init__(self, output_dir="nasa_power_data", database_file="district_database.csv", merged_file="merged_all_districts.csv", params_file=None):
        self.output_dir = output_dir
        self.database_file = database_file
        self.merged_file = merged_file
        self.base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        self.df_database = pd.read_csv(database_file)
        os.makedirs(self.output_dir, exist_ok=True)

        # Define default API parameters
        self.default_params = {
            "start": "20040101",  # YYYYMMDD
            "end": "20240801",
            "community": "ag",
            "parameters": "ALLSKY_SFC_SW_DWN,CLRSKY_SFC_SW_DWN,ALLSKY_SFC_PAR_TOT,ALLSKY_SFC_UV_INDEX,"
                          "T2M,T2MDEW,TS,T2M_RANGE,QV2M,RH2M,PRECTOTCORR,PS,WS2M,WD2M,GWETTOP,GWETROOT,GWETPROF",
            "format": "csv",
            "header": "true"
        }

        # Load params from JSON if specified
        self.params = self.load_params(params_file) if params_file else self.default_params

    def load_params(self, params_file):
        """Load API parameters from a JSON file."""
        if not os.path.exists(params_file):
            raise FileNotFoundError(f"JSON file {params_file} not found.")
        
        with open(params_file, 'r') as file:
            params = json.load(file)
        print(f"Loaded parameters from {params_file}")
        return params

    def merge_csv_files(self):
        """Merge all CSV files from the output directory into one CSV file."""
        all_dataframes = []
        csv_files = [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir) if f.endswith(".csv")]
        
        for file in csv_files:
            df = pd.read_csv(file)
            all_dataframes.append(df)

        if all_dataframes:
            merged_df = pd.concat(all_dataframes, ignore_index=True)
            merged_df.to_csv(self.merged_file, index=False)
            print(f"✔ Merged CSV saved as {self.merged_file}")
        else:
            print("No CSV files found to merge.")

    def add_location_data(self):
        """Add location information (latitude, longitude) from the district database to the CSV files."""
        for file in os.listdir(self.output_dir):
            if file.endswith(".csv"):
                district_name = file.replace(".csv", "")  # Extract district name
                
                # Find corresponding district info
                district_info = self.df_database[self.df_database["District"] == district_name]
                if district_info.empty:
                    print(f"No matching district found for {district_name}")
                    continue

                lat, lon = district_info.iloc[0]["Latitude"], district_info.iloc[0]["Longitude"]
                
                # Read the existing CSV
                file_path = os.path.join(self.output_dir, file)
                df = pd.read_csv(file_path)
                
                # Insert new columns for district name, latitude, and longitude
                df.insert(0, "Region", district_name)
                df.insert(1, "Latitude", lat)
                df.insert(2, "Longitude", lon)

                # Save the updated file
                df.to_csv(file_path, index=False)
                print(f"Updated file: {file_path}")

    def download_nasa_data(self, district, lat, lon):
        """Download NASA Power API data for the given district and save it as a CSV file."""
        params = self.params.copy()
        params["latitude"] = lat
        params["longitude"] = lon
        
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            filename = os.path.join(self.output_dir, f"{district}.csv")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"Data saved: {filename}")
        else:
            print(f"Failed to retrieve data for {district} ({lat}, {lon}) - Status Code: {response.status_code}")

    def download_data_for_all_districts(self):
        """Download NASA data for all districts listed in the district database."""
        for _, row in self.df_database.iterrows():
            self.download_nasa_data(row["District"], row["Latitude"], row["Longitude"])

    def clean_csv_files(self):
        """Remove the first 25 rows from all CSV files in the output directory."""
        for file in os.listdir(self.output_dir):
            if file.endswith(".csv"):
                file_path = os.path.join(self.output_dir, file)
                df = pd.read_csv(file_path, skiprows=25)
                df.to_csv(file_path, index=False)
                print(f"Cleaned and saved: {file_path}")


    # Initialize the processor object with a custom params JSON file (optional)
    #processor = Processor(params_file="custom_params.json")

    # Uncomment the following lines to perform different operations:
    
    # Merge CSV files
    # processor.merge_csv_files()

    # Add location data to the CSV files
    # processor.add_location_data()

    # Download data for all districts
    # processor.download_data_for_all_districts()

    # Clean CSV files (remove first 25 rows)
    # processor.clean_csv_files()
