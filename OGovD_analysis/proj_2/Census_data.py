"""
Analysis and visualization
idea to analyze census data from AP, Visakhapatnam
Link: https://ap.data.gov.in/resource/villagetown-wise-primary-census-abstract-2011-visakhapatnam-district-andhra-pradesh

"""
import requests
import pandas as pd
from config import API_INFO

census_url = "https://api.data.gov.in/resource/7360817d-7c02-4e0d-9143-976741df656e?"

params = {
    "api-key": API_INFO["api_key"],
    "format": "json",
    "limit": 10000
}

response = requests.get(census_url, params=params)
data = response.json()
print(data["total"])
#print(data["records"].columns())

df = pd.DataFrame(data["records"])
print(df.head())

# In data understanding it is noticed that few of the metric columns are non-numeric so need perform data cleaning
""" Data Cleaning: converting the non numeric columns to numeric and deleting the rows consisting all zero columns"""
# Convert all columns to numeric where possible
df = df.apply(pd.to_numeric, errors='coerce')
# print(df.columns)

# Drop rows where all metric values are zero (assuming 'state_uts_code' and 'district_code' are non-metric)
metric_columns = ['total_population_person', "total_population_male", "total_population_female"]
df = df[~(df[metric_columns].fillna(0).eq(0).all(axis=1))]


# Performing some basic descriptive analysis
def calculate_basic_stats(data: pd.DataFrame):
    total_population = df.groupby(["state_uts_code", "district_code"]).agg(
        {"total_population_person": "sum"})
    avg_population = df.groupby(["state_uts_code", "district_code"])["total_population_person"].mean()
    return total_population, avg_population

print(calculate_basic_stats(df))


"""
next steps:
During data understanding found some anamolies try correct them and finish the descriptive analysis
"""
