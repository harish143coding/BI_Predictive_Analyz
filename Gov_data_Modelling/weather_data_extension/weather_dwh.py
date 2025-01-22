"""
GOAL: BHARAT MAUSAM ki DATAWAREHOUSE
In weather data model package a tiny dwh for the weather data i.e. rainfall from 2023 November  is loaded
Idea -> how to scale the warehouse with further rainfall data
Brainstorming
1. Dataset from API: https://api.data.gov.in/catalog/a6007b2f-eed3-4a68-a321-d2d563d52bb2? this API consists of avg_rainfall
   data for all the states approx until 2023. (site: https://www.data.gov.in/apis/a6007b2f-eed3-4a68-a321-d2d563d52bb2)
2. how can I get statewise temperature historical data, so that fact data contains values of monthly temperature state-wise?

PROMPT: I have a dataframe consisting mean temperatures of India over a time period from 1901 to 2021. now can you
        calcuate the mean temperature state-wise for all the 29 Indian
       states using any suitable algorithm based on the geographical location the states such that considering states
       in the north are with bit lower temperatures compared to the southern states.

"""
from shapely.geometry import Point
from state_weights import state_weights
import pandas as pd
import geopandas as gpd


# Load temperature data (assumed to have 'latitude', 'longitude', 'temperature')
df = pd.read_csv("TEMP_ANNUAL_MEAN_1901-2021.csv")  # Replace with actual file path
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
print(state_mean_temp_df.describe())

"""
next steps:
new dataframe is created with year,state, monthwise mean temperature.
Next: what facts are further needed for the Mausam DWH?
"""