"""
Brainstorming:
On which data from the Open Govt Data portal should be worked on?
1. https://data.gov.in/
2. There datasets classified under 36 public departments
3. for the first choosing the department of Labour and employment.
  - for the first analysis data from the following link be used
  "https://www.data.gov.in/resource/state-wise-jobseeker-registration-ncs-portal-till-30-june-2022"
4. Visualization: The idea is to present the results on Indian map.
"""
from pprint import pprint
from config import API_INFO
from Geo_coordinates_India import geo_coordinates
import requests
import pandas as pd
import folium

# Define the API endpoint and your API key
api_url = "https://api.data.gov.in/resource/a79d3456-edcc-4c52-9be8-7682476cb64a?"
api_key = API_INFO["Employment_api_key"]
format_type = "json"

params = { "api-key": api_key,
           "format": "json",
           "limit": 1000}

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
#pprint(data)
df = pd.DataFrame(data['records'])


# Add geo-coordinates to the DataFrame
df['Latitude'] = df['states'].map(lambda x: geo_coordinates[x][0])
df['Longitude'] = df['states'].map(lambda x: geo_coordinates[x][1])


# Create a base map
india_map = folium.Map(location=[20.5937, 78.9629], tiles="OpenStreetMap", zoom_start=5)


# Add the GeoJSON layer for India
india_geojson = './india_state_geo.json'
folium.GeoJson(india_geojson).add_to(india_map)


# Add markers to the map
kw = {"prefix": "fa", "color": "green", "icon": "arrow-up"}

for idx, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['states']}: {row['female']}",
        icon = folium.Icon(angle=row['states'], **kw)
    ).add_to(india_map)


# Set the map bounds to focus on India
bounds = [[6.5, 68.0], [35.5, 97.5]] # Approximate bounds for India
india_map.fit_bounds(bounds)

# Save the map to an HTML file
india_map.save('india_map_with_coordinates.html')

india_map





