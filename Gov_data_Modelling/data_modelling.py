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
        print(data["total"])
        print(data["count"])
        print(data["limit"])
        #print(len(data["records"]))

        if not data:
            break  # No more records to retrieve

        all_records.extend(data)
        offset += params['limit']

    return all_records


# Example usage
all_records = get_all_records()

print(type(all_records))
# print(len(all_records['records']))
# df = pd.DataFrame(all_records['records'])
# print(df.head())
# print(df.info())
# print(df["avg_rainfall"].unique())




"""
Next steps:
FOKUS: here the idea is data engineering so data content is less bothered
it is observed from the json keys 'total' records '21990'.
then new function should be tested. 
"""