"""
the idea is to carry-out appropriate visualization preferably Geo-Visualization if no the other
Dataset (Gross State Domestic Product): https://www.data.gov.in/resource/gross-state-domestic-product-gsdp-current-prices-states-and-uts-2011-12-2021-22
"""
from OGovD_analysis.config import API_INFO
import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


gsdp_url = "https://api.data.gov.in/resource/adb4b1da-159f-46b3-a9c0-0545fe9ddda0?"

params = {
    "api-key": API_INFO["api_key"],
    "format": "json",
    "limit": 10000
}

response = requests.get(gsdp_url, params=params)
data = response.json()
print(type(data["records"][0]))


# Load shapefile for Indian states
india_states = gpd.read_file('OGovD_analysis/proj_3_national_population/India Shape/india_st.shp')
print(india_states["STATE"])

# Load GDP data
gdp_data = pd.DataFrame(data["records"])
# Mapping the state names according to GeoDataFrame from the States shape file.
state_name_mapping = {
    "Odisha": "Orissa",
    "Chhattisgarh": "CHANDIGARH",
    # Add other mappings
}

gdp_data['state_uts'] = gdp_data['state_uts'].replace(state_name_mapping)
gdp_data['state_uts'] = gdp_data['state_uts'].str.upper()



unmatched_states = set(gdp_data['state_uts']) - set(india_states['STATE'])
print("Unmatched states:", unmatched_states)


# Merge GDP data with shapefile
merged = india_states.merge(gdp_data, left_on='STATE', right_on='state_uts')

# Plot choropleth map
merged.plot(column='gsdp_curr_2021_22_cr_', cmap='OrRd', legend=True)
plt.title("Indian States GDP for 2021-22")
plt.show()






"""
Next steps:
geovisualization should be adusted by correcting the state names
"""