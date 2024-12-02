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


# define the API endpoint and your API key. here weather data
weather_api_endpoint = "https://api.data.gov.in/resource/b3521980-43d8-4d22-b86e-43f9a927f4b9?"

parameters = {
                "api_key": API_INFO["weather_api_key"],
                "format": "json",
                "limit": 1000
}

# Make the GET request to the API with parameters
response = requests.get(weather_api_endpoint, params=parameters)


# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Print the retrieved data
    print(type(data))
else:
    print(f"Failed to retrieve data: {response.status_code}")


"""
Next steps:
test the API:
find the error
may be error in api_key or URL?
"""