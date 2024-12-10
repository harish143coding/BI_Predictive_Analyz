"""
Brainstorming : the idea is to go through the data in open Gov data and prepare a tiny Data warehouse
--> Data Understanding
        --> Modelling
                --> ETL pipeline
                            --> Testing
Data resource: weather data from the below link
https://www.data.gov.in/resource/daily-rainfall-data-national-remote-sensing-centre-nrsc-vic-model-agency-during-november-4
"""
from config import API_INFO, DB_CONFIG
from sqlalchemy import create_engine
import requests
import pandas as pd


# define the API endpoint and your API key. here weather data
weather_api_endpoint = "https://api.data.gov.in/resource/b3521980-43d8-4d22-b86e-43f9a927f4b9?"


def get_all_records(api_url) -> pd.DataFrame:
    """
    performing pagination to retrieve all the records from the API
    NOTE: only able to retrieve first 10,000 records (to test API_TESTER.py is used) problem with the API provider.
    API : api URL
    output: returns the data records dataframe
    """
    params = {
        "api-key": API_INFO["weather_api_key"],
        "format": "json",
        "limit": 10000  # Adjust this value based on the APIs maximum limit
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    print(data.keys())
    data_records = data["records"]
    df = pd.DataFrame(data_records)
    return df


# Example usage
df = get_all_records(weather_api_endpoint)
print(df.head())


"""
PART-2: Building the ETL process 
Now the idea is to create a data model for weather data
Dimensions : Location, Time
Fact: weather facts
"""

# Convert the 'date' column to datetime
df['datetime'] = pd.to_datetime(df['date'])
df['date'] = df['datetime'].dt.date
df['time'] = df['datetime'].dt.time

# Location Dimension
location_df = df[['_state_', 'district']].drop_duplicates().reset_index(drop=True)
location_df['location_id'] = location_df.index + 1

# Time Dimension
time_df = df[['date', 'time', 'year', 'month']].drop_duplicates().reset_index(drop=True)
time_df['time_id'] = time_df.index + 1

# Fact Table
fact_df = df.merge(location_df, on=['_state_', 'district'], how='left')
fact_df = fact_df.merge(time_df, on=['date', 'time', 'year', 'month'], how='left')
fact_df = fact_df[[
    'location_id', 'time_id', 'avg_rainfall', 'agency_name'
]]

from sqlalchemy import create_engine

# Replace these variables with your database credentials
db_type = 'mysql'  # or 'postgresql', 'sqlite', etc.
db_user = 'your_username'
db_password = 'your_password'
db_host = 'localhost'
db_name = 'your_db_name'

engine = create_engine(f'{db_type}://{db_user}:{db_password}@{db_host}/{db_name}')

# Loading data into the database
location_df.to_sql('location_dim', engine, if_exists='replace', index=False)
time_df.to_sql('time_dim', engine, if_exists='replace', index=False)
fact_df.to_sql('rainfall_fact', engine, if_exists='replace', index=False)





"""
Next steps:
FOKUS: here the idea is data engineering so data content is less bothered
next step storing the data according to dimensions after data understanding.
"""