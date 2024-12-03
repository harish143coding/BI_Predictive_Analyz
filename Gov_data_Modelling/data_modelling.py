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



parameters = {
                "api-key": API_INFO["weather_api_key"],
                "format": "json",
               "limit": 10000  # for scaling the database how to retrieve the further records
}

# Make the GET request to the API with parameters
response = requests.get(weather_api_endpoint, params=parameters)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Print the retrieved data
    print(type(response))
else:
    print(f"Failed to retrieve data: {response.status_code}")


print(len(data['records']))
df = pd.DataFrame(data['records'])
print(df.head())
print(df.info())
print(df.groupby(["_state_"]).mean("avg_rainfall"))



"""
Next steps:
test the API:
go through the rainfall data from the dataframe it looks like the same avg rainfall in all the states
"""