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
print(df.head())


# Create a DataFrame with states and their weights
state_df = pd.DataFrame(list(state_weights.items()), columns=["state_name", "weight"])

# Calculate the adjusted annual temperature for each state
state_mean_temp = []
for state, weight in state_weights.items():
    # Adjust the ANNUAL temperature based on the weight
    adjusted_temps = df["ANNUAL"] * weight
    mean_temp = adjusted_temps.mean()
    state_mean_temp.append({"state_name": state, "mean_temperature": mean_temp})

# Create a DataFrame for state-wise mean temperatures
state_mean_temp_df = pd.DataFrame(state_mean_temp)

# Save results to a CSV
state_mean_temp_df.to_csv("state_mean_temperatures.csv", index=False)

# Output results
print(state_mean_temp_df)




"""
next steps:
reusing the configs for API and DB how?

re-evaluated the code in ChatGPT now should work on the new one.
"""