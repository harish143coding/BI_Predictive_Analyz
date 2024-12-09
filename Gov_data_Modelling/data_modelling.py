"""
Brainstorming : the idea is to go through the data in open Gov data and prepare a tiny Data warehouse
--> Data Understanding
        --> Modelling
                --> ETL pipeline
                            --> Testing
Data resource: weather data from the below link
https://www.data.gov.in/resource/daily-rainfall-data-national-remote-sensing-centre-nrsc-vic-model-agency-during-november-4
"""
from config import API_INFO
import requests
import pandas as pd


# define the API endpoint and your API key. here weather data
weather_api_endpoint = "https://api.data.gov.in/resource/b3521980-43d8-4d22-b86e-43f9a927f4b9?"


def get_all_records():
    """
    performing pagination to retrieve all the records from the API
    """
    params = {
        "api-key": API_INFO["weather_api_key"],
        "format": "json",
        "limit": 10000  # Adjust this value based on the APIs maximum limit
    }
    offset = 0
    all_records = []

    while True:
        params['offset'] = offset
        response = requests.get(weather_api_endpoint, params=params)
        data = response.json()
        print(data.keys())
        #print(len(data["records"]))
        print(data["message"])

        if 'records' not in data or not data['records']:
            break  # No more records to retrieve

        all_records.extend(data["records"])
        offset += len(data['records'])

    return all_records


# Example usage
all_records = get_all_records()

print(type(all_records))
print(len(all_records['records']))



"""
Next steps:
FOKUS: here the idea is data engineering so data content is less bothered
only able to retrieve first 10,000 records (to test API_TESTER.py is used) problem with the API povider.
next step storing the data according to dimensions after data understanding.
"""