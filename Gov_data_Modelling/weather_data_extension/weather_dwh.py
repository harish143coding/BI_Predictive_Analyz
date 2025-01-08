"""
GOAL: BHARAT MAUSAM ki DATAWAREHOUSE
In weather data model package a tiny dwh for the weather data i.e. rainfall from 2023 November  is loaded
Idea -> how to scale the warehouse with further rainfall data
Brainstorming
1. Dataset from API: https://api.data.gov.in/catalog/a6007b2f-eed3-4a68-a321-d2d563d52bb2? this API consists of avg_rainfall
   data for all the states approx until 2023. (site: https://www.data.gov.in/apis/a6007b2f-eed3-4a68-a321-d2d563d52bb2)
2. how can I get statewise temperature historical data, so that fact data contains values of monthly temperature state-wise?

"""
import pandas as pd

weather_df = pd.read_csv("TEMP_ANNUAL_MEAN_1901-2021.csv")

print(weather_df.head())

import pandas as pd

# Given dataframe with country's mean temperature
data = {
    'YEAR': [1901, 1902, 1903, 1904],
    'JAN': [19.32, 20.17, 19.28, 19.19],
    'FEB': [20.89, 21.58, 20.71, 20.32],
    # Add all other months
}
df = pd.DataFrame(data)

# List of Indian states
states = ['State1', 'State2', 'State3']  # Replace with actual state names

# Replicate the country's mean temperature data for each state
statewise_data = []
for state in states:
    state_df = df.copy()
    state_df['STATE'] = state
    statewise_data.append(state_df)

# Concatenate all statewise data into a single dataframe
df_states = pd.concat(statewise_data)

# Calculate the state-wise mean temperatures
statewise_mean_temperatures = df_states.groupby('STATE').mean()

# Print the result
print(statewise_mean_temperatures)

"""
next steps:
reusing the configs for API and DB how?
find the resource for temperatures monthly state wise

using the mean temperature data of india states temperature shoould be caculated. 
"""