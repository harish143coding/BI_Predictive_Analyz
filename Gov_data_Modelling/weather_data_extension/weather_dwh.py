"""GOAL: BHARAT MAUSAM ki DATAWAREHOUSE In weather data model package a tiny dwh for the weather data i.e. rainfall
from 2023 November  is loaded Idea -> how to scale the warehouse with further rainfall data Brainstorming

1. how can I get state-wise temperature historical data, so that fact data contains values of monthly temperature
state-wise. Extract step is done Solu- Func 1 get_temperature_data is created
  - Check and Transform the Dataframe
  - fter that schema should be desine and Load should be executed
2. Dataset from API: https://api.data.gov.in/catalog/a6007b2f-eed3-4a68-a321-d2d563d52bb2? this API consists of avg_rainfall
data for all the states approx until 2023. (site: https://www.data.gov.in/apis/a6007b2f-eed3-4a68-a321-d2d563d52bb2)
Extract step is done Solu - Func 2: process_mean_rainfall_data is created
  - In Transform step Dataframe shoud be vaidated and  'NA' rows shoud be deleted
  - After that schema should be desine and Load should be executed
ETL - Extra for first two facts is done.
3. the idea is to load atleast data last 40 years from 1980, so that in future ML models can be trained.
4. AQI data is only available from 2015 to 2020 for few stations from the folowing source
https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india/data?select=station_day.csv



available facts : Mean Temperature monthly, state-wise from 1901 to 2021
                 Avg Rainfall state-wise
                 AQI data
                 next important?

"""
from Gov_data_Modelling.weather_data_extension.state_weights import state_weights, Indian_states
from Gov_data_Modelling.config import API_INFO
import requests
import pandas as pd
import geopandas as gpd


def get_temperature_data(source_file):
    """
    this Func takes the raw temperature data from the OGoV portal and gives out mean temperature monthly, state-wise
    from 1901 to 2021

    returns a Dataframe with mean temperature data
    """
    # Load temperature data (assumed to have 'latitude', 'longitude', 'temperature')
    df = pd.read_csv(source_file)  # Replace with actual file path
    df.drop(columns=["JAN-FEB", "MAR-MAY", "JUN-SEP", "OCT-DEC"], inplace=True)

    state_mean_temp = []

    # List of month columns
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    # Ensure monthly and annual columns are numeric
    for month in months:
        df[month] = pd.to_numeric(df[month], errors="coerce").fillna(0)
    df["ANNUAL"] = pd.to_numeric(df["ANNUAL"], errors="coerce").fillna(0)

    # Ensure weights are numeric
    state_weights_1 = {state: float(weight) for state, weight in state_weights.items()}

    # Loop through states to calculate adjusted mean temperatures
    for state, weight in state_weights_1.items():
        for year in df["YEAR"].unique():
            state_data = {"state_name": state, "year": year}

            # Filter data for the current year
            year_data = df[df["YEAR"] == year]

            # Calculate adjusted mean temperature for each month
            for month in months:
                adjusted_temps = year_data[month] * weight  # Adjust using weight
                mean_temp = adjusted_temps.mean()  # Compute the mean
                state_data[f"mean_temperature_{month}"] = mean_temp  # Add monthly mean

            # Calculate adjusted annual mean temperature
            adjusted_annual = year_data["ANNUAL"] * weight
            state_data["mean_temperature_annual"] = adjusted_annual.mean()

            # Append state data to results
            state_mean_temp.append(state_data)

    state_mean_temp_df = pd.DataFrame(state_mean_temp)
    return state_mean_temp_df


temperature_data_source = "TEMP_ANNUAL_MEAN_1901-2021.csv"

# testing the first fn in Bharat Mausam Dwh
temperature_df = get_temperature_data(temperature_data_source)


def process_mean_rainfall_data(api_endpoint, start_year, end_year):
    """
    The purpose of this Func is to fetch the raw rainfall data from the API and obtain
    state-wise, monthly rainfall data
    arguments
    Api_endpoint: endpoint of the available API
    start_year: the first year from which the average rainfall_data needed to be fetched from the API
    end_year: similarly last year
    returns: length of the total records fetched and dataframe with mean rainfall state-wise
    """
    params = {
        "api-key": API_INFO["weather_api_key"],
        "format": "json",
        "scroll": "1m",
        "limit": 10000  # Ensure this matches the API's maximum limit
    }
    all_data = []
    start_year = start_year  # Adjust based on API data range
    end_year = end_year  # Set to the latest year available
    a = Indian_states[1:-1].split("' '")
    # Cleaning up quotes and spaces
    states = [name.strip("' ") for name in a]

    for state in states:
        for year in range(start_year, end_year + 1):
            offset = 0
            while True:
                params.update({
                    "filters[year]": year,  # Correct API format
                    "filters[_state_]": state,  # Correct API format
                    "offset": offset
                })

                response = requests.get(api_endpoint, params=params)

                if response.status_code != 200:
                    print(f"Error: {response.status_code}, {response.text}")
                    break

                data = response.json()

                if "records" not in data or not data["records"]:
                    break  # Stop if no more records

                all_data.extend(data["records"])

                print(f"Fetched {len(all_data)} records for {state}, {year}...")

                if len(data["records"]) < 1000:  # If fewer than limit, stop
                    break

                offset += 1000  # Move to the next batch

        df = pd.DataFrame(all_data)
    return print(f"Total records fetched: {len(all_data)}"), df


# Test the Rainfall function
rainfall_api_endpoint = "https://api.data.gov.in/catalog/a6007b2f-eed3-4a68-a321-d2d563d52bb2?"
total_records, rainfall_df = process_mean_rainfall_data(rainfall_api_endpoint, 2022, 2023)
#print(len(y), y["_state_"].unique())


# Func to Extract AQI data from Indian data portal
"""
func shoud be formuated to etract AQI data
stations should be mapped
"""


def process_aqi_data(input_file_1, input_file_2):
    """
    this Func takes AQI data from a 2 CSV inputs one with various AQI metrics and station ID
    and other file with station geographical information

    returns: a merged AQI DF after processing both files
    """

    aqi_data = pd.read_csv(input_file_1)
    aqi_data.drop(columns=["Benzene", "Toluene", "Xylene"], inplace=True)
    aqi_stations = pd.read_csv(input_file_2)
    final_aqi_df = aqi_data.merge(right=aqi_stations, how="outer", on="StationId")
    return final_aqi_df


#  func 3
file_1 = "station_day.csv"
file_2 = "stations.csv"
aqi_df = process_aqi_data(file_1, file_2)
aqi_df.describe()
"""
next steps: 
"""
