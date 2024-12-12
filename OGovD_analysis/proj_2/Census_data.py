"""
Analysis and visualization
idea to analyze census data from AP, Visakhapatnam
Link: https://ap.data.gov.in/resource/villagetown-wise-primary-census-abstract-2011-visakhapatnam-district-andhra-pradesh

"""
from config import API_INFO
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



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
# creating a bar graphh
plt.figure(figsize=(10, 6))
sns.barplot(x='mandal_code', y='total_population_person', data=df)
plt.title('Total Population per Mandal')
plt.xlabel('Mandal Code')
plt.ylabel('total_population_person')
plt.show()

# Visualization for avg population
tota_popi, avg_popi = calculate_basic_stats(df)
plt.figure(figsize=(8, 8))
plt.pie(avg_popi, labels=df['mandal_code'], autopct='%1.1f%%')
plt.title('Distribution of Average Population per Mandal')
plt.show()


# Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x=[coord[1] for coord in df['geo_coordinates']], y=[coord[0] for coord in df['geo_coordinates']], size='total_population', hue='total_population', data=df, legend=False, sizes=(20, 200))
plt.title('Geo Coordinates vs Total Population')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df[['total_population', 'avg_population']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Between Metrics')
plt.show()



"""
next steps:
rest of the visualization should be tested and published
"""
