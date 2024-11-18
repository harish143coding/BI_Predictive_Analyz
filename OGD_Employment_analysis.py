"""
Brainstorming:
On which data from the Open Govt Data portal should be worked on?
1. https://data.gov.in/
2. There datasets classified under 36 public departments
3. for the first choosing the department of Labour and employment.
  - for the first analysis data from the follwing link be used
  "https://www.data.gov.in/resource/state-wise-jobseeker-registration-ncs-portal-till-30-june-2022"
"""
import pandas as pd
from pprint import pprint
from config import API_INFO
import requests

# Define the API endpoint and your API key
api_url = "https://api.data.gov.in/resource/a79d3456-edcc-4c52-9be8-7682476cb64a?"
api_key = API_INFO["Employment_api_key"]
format_type = "json"

params = { "api-key": api_key,
           "format": "json" }

# Set the headers including the API key
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": f"application/{format_type}"
}

# Make the GET request to the API with headers
response = requests.get(api_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Print the retrieved data
    print(type(data))
else:
    print(f"Failed to retrieve data: {response.status_code}")


print(data.keys())
#print(data['records'])
#pprint(data['records'])
df = pd.DataFrame(data['records'])
print(df.head())


