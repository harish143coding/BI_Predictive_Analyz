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
import pandas as pd

weather_df = pd.read_csv("TEMP_ANNUAL_MEAN_1901-2021.csv")

print(weather_df.head())

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load temperature data (assumed to have 'latitude', 'longitude', 'temperature')
data = pd.read_csv("temperature_data.csv")  # Replace with actual file path
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.longitude, data.latitude))

# Load shapefile for Indian states (replace 'states_shapefile.shp' with actual path)
states_gdf = gpd.read_file("states_shapefile.shp")

# Spatial join to assign each temperature point to a state
gdf = gpd.sjoin(gdf, states_gdf, how="left", op="within")

# Add latitude-based adjustment factor (normalize latitude for adjustment)
def calculate_adjustment(lat):
    """Lower latitudes (southern states) get a higher adjustment."""
    max_lat, min_lat = 37.6, 8.4  # Approx latitude range for India
    return 1 + (lat - min_lat) / (max_lat - min_lat) * 0.2  # Example scaling

gdf["adjustment_factor"] = gdf["latitude"].apply(calculate_adjustment)
gdf["adjusted_temperature"] = gdf["temperature"] * gdf["adjustment_factor"]

# Group by state and calculate mean temperature
state_mean_temp = gdf.groupby("state_name").agg({
    "adjusted_temperature": "mean"
}).reset_index()

state_mean_temp.rename(columns={"adjusted_temperature": "mean_temperature"}, inplace=True)

# Save results
state_mean_temp.to_csv("state_mean_temperatures.csv", index=False)
print(state_mean_temp)





"""
next steps:
reusing the configs for API and DB how?
find the resource for temperatures monthly state wise

using the mean temperature data of india states temperature should be calculated. 
"""