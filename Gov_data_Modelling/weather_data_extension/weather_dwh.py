"""
GOAL: BHARAT MAUSAM ki DATAWAREHOUSE
In weather data model package a tiny dwh for the weather data i.e. rainfall from 2023 November  is loaded
Idea -> how to scale the warehouse with further rainfall data
Brainstorming
1. Dataset from API: https://api.data.gov.in/catalog/a6007b2f-eed3-4a68-a321-d2d563d52bb2? this API consists of avg_rainfall
   data for all the states approx until 2023. (site: https://www.data.gov.in/apis/a6007b2f-eed3-4a68-a321-d2d563d52bb2)
2. how can I get statewise temperature historical data, so that fact data contains values of monthly temperature state-wise?

avaiable facts : Mean Temperature monthly, statewise from 1901 to 2021
                 Avg Rainfall statewise
                 next important?

"""
from shapely.geometry import Point
from Gov_data_Modelling.weather_data_extension.state_weights import state_weights
from Gov_data_Modelling.config import API_INFO
import requests
import pandas as pd
import geopandas as gpd


def get_temperature_data(source_file):
    """
    this Func takes the raw temperature data from the OGoV portal and gives out mean temperature monthy, statewise
    from 1901 to 2021
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
# print(get_temperature_data(temperature_data_source).head())

def process_mean_rainfal_data(API_endpoint):
    """
    The purpose of this Func is to fetch the raw rainfall data from the API and obtain
    statewise, monthly rainfall data
    """
    params = {
        "api-key": API_INFO["weather_api_key"],
        "format": "json",
        "scroll": "1m",
        "limit": 10000  # Ensure this matches the API's maximum limit
    }
    all_data = []
    offset = 0

    while True:
        params["offset"] = offset  # Add offset for pagination
        response = requests.get(API_endpoint, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break  # Stop if there’s an error

        data = response.json()
        if "records" not in data or not data["records"]:  # Ensure 'records' exists
            break  # Stop if no more records are available

        all_data.extend(data["records"])  # Append only the records list

        if len(data["records"]) < 10000:  # Stop when fewer than 10,000 records are returned
            break
        print(data["total"])
        offset += 10000  # Move to the next batch



    #df = pd.DataFrame(all_data["records"])
    return print(f"Total records fetched: {len(all_data)}")


# Test the Rainfall function
rainfall_api_endpoint = "https://api.data.gov.in/catalog/a6007b2f-eed3-4a68-a321-d2d563d52bb2?"
print(process_mean_rainfal_data(rainfall_api_endpoint))

"""
next steps:
first function for Temperature facts dataframe is created with year,state, monthwise mean temperature.
Nextstep: execute the code and ask this error in ChatGPT difference between the total and records
"""
