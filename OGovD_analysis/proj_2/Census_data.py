"""
Analysis and visualization
idea to analyze census data from AP, Visakhapatnam
Link: https://ap.data.gov.in/resource/villagetown-wise-primary-census-abstract-2011-visakhapatnam-district-andhra-pradesh

"""
from config import API_INFO
import geopandas as gpd
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap



census_url = "https://api.data.gov.in/resource/7360817d-7c02-4e0d-9143-976741df656e?"

params = {
    "api-key": API_INFO["api_key"],
    "format": "json",
    "limit": 10000
}

response = requests.get(census_url, params=params)
data = response.json()
print(data["total"])


df = pd.DataFrame(data["records"])
print(df.head())
df.rename(columns={"cd_block_code": "mandal_code"},  inplace=True)

# In data understanding it is noticed that few of the metric columns are non-numeric so need perform data cleaning
""" Data Cleaning: converting the non numeric columns to numeric and deleting the rows consisting all zero columns """
# Convert all columns to numeric where possible
df = df.apply(pd.to_numeric, errors='coerce')

# Function to generate approximate geo-coordinates (example logic)
def generate_geo_coordinates(mandal_code):
    base_lat = 17.6868  # Base latitude for Visakhapatnam
    base_lon = 83.2185  # Base longitude for Visakhapatnam
    offset = (mandal_code - 516) * 0.01  # Increment latitude and longitude slightly per code
    return f"{base_lat + offset:.4f}°N, {base_lon + offset:.4f}°E"

# Adding Geo Coordinates column
df['Geo Coordinates']= df["mandal_code"].apply(generate_geo_coordinates)



# Drop rows where all metric values are zero (assuming 'state_uts_code' and 'district_code' are non-metric)
metric_columns = ['total_population_person', "total_population_male", "total_population_female"]
df = df[~(df[metric_columns].fillna(0).eq(0).all(axis=1))]


# Performing some basic descriptive analysis
def calculate_basic_stats(data: pd.DataFrame):
    total_population = df.groupby(["state_uts_code", "district_code", "mandal_code"]).agg(
        {"total_population_person": "sum"})
    avg_population = df.groupby(["state_uts_code", "district_code", "mandal_code"])["total_population_person"].mean()
    return total_population, avg_population

print(calculate_basic_stats(df))
print(f" Distinct values in column {"mandal_code"} are {df["mandal_code"].unique()}")
print(f" Distinct values in column {"town_village_code"} are {df["town_village_code"].unique()}")


""" Visualizations """
#1 creating a bar graphh
plt.figure(figsize=(10, 6))
sns.barplot(x='mandal_code', y='total_population_person', data=df)
plt.title('Total Population per Mandal')
plt.xlabel('Mandal Code')
plt.ylabel('total_population_person')
plt.show()

#2 Visualization for avg population
tot_popi, avg_popi = calculate_basic_stats(df)
plt.figure(figsize=(8, 8))
plt.pie(avg_popi, labels=df['mandal_code'].unique(), autopct='%1.1f%%')
plt.title('Distribution of Average Population per Mandal')
plt.show()


#3 Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x=[coord[1] for coord in df["Geo Coordinates"]], y=[coord[0] for coord in df["Geo Coordinates"]], size='total_population_person', hue='total_population_person', data=df, legend=False, sizes=(20, 200))
plt.title('Geo Coordinates vs Total Population')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

#4 Heatmap
plt.figure(figsize=(8, 6))
sns.regplot(x='total_population_male', y='total_population_female', data=df)
plt.title('Correlation between Total Male and Female Population')
plt.show()

#5 Geo Mapping
df['latitude'] = df["Geo Coordinates"].apply(lambda x: x[0])
df['longitude'] = df["Geo Coordinates"].apply(lambda x: x[1])

# Load the shapefile (replace 'path_to_shapefile' with the actual path)

shapefile_path = 'india_District_level_2.shp'
mandal_gdf = gpd.read_file(shapefile_path)
mandal_gdf['mandal_code'] = df['mandal_code']

# Merge the shapefile GeoDataFrame with your data
merged_gdf = mandal_gdf.merge(df, on='mandal_code')


# Initialize the map centered around Visakhapatnam
m = folium.Map(location=[17.6868, 83.2185], zoom_start=10)

# Convert GeoDataFrame to GeoJSON for Folium
geojson = merged_gdf.to_crs(epsg=4326).to_json()

# Add GeoJSON layer to the map
folium.GeoJson(geojson, name="Mandal Boundaries").add_to(m)

# Prepare data for the HeatMap
heat_data = [[row['latitude'], row['longitude'], row['total_population_male']] for index, row in df.iterrows()]

# Add HeatMap layer to the map
HeatMap(heat_data).add_to(m)

# Add layer control to toggle between layers
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('visakhapatnam_mandal_heatmap.html')


"""
next steps:

All the visualizations are working except the Map with shape file on mandal coordinates
"""
