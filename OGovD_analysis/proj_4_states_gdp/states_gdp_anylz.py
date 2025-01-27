"""
the idea is to carry-out appropriate visualization preferably Geo-Visualization if no the other
Dataset (Gross State Domestic Product): https://www.data.gov.in/resource/gross-state-domestic-product-gsdp-current-prices-states-and-uts-2011-12-2021-22

Brainstorming:
1. The idea is to carry out 2-3 appropriate visualizations with this data.(1 is already created)
2. shape file should e fitted according to the new states

"""
from OGovD_analysis.config import API_INFO
from OGovD_analysis.India_Geo_Coords import geo_coordinates
import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium


gsdp_url = "https://api.data.gov.in/resource/adb4b1da-159f-46b3-a9c0-0545fe9ddda0?"
def get_GDP_choropleth_visual(api_url):
    """
    Func to get choropleth visualization
    """

    params = {
        "api-key": API_INFO["api_key"],
        "format": "json",
        "limit": 10000
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    # Load shapefile for Indian states
    india_states = gpd.read_file('OGovD_analysis/proj_3_national_population/India Shape/india_st.shp')
    print(india_states["STATE"])

    # Load GDP data
    gdp_data = pd.DataFrame(data["records"])
    print(gdp_data.head())
    # Mapping the state names according to GeoDataFrame from the States shape file.
    state_name_mapping = {
        "Odisha": "Orissa",
        "Chhattisgarh": "CHANDIGARH",
        "Jammu & Kashmir*": "JAMMU AND KASHMIR",
        "Andaman & Nicobar Islands": "ANDAMAN AND NICOBAR ISLANDS",
        "Puducherry": "PONDICHERRY"
        # Add other mappings
    }

    gdp_data['state_uts'] = gdp_data['state_uts'].replace(state_name_mapping)
    gdp_data['state_uts'] = gdp_data['state_uts'].str.upper()

    unmatched_states = set(gdp_data['state_uts']) - set(india_states['STATE'])
    print("Unmatched states:", unmatched_states)

    # Merge GDP data with shapefile
    merged = india_states.merge(gdp_data, left_on='STATE', right_on='state_uts')

    # Plot choropleth map
    merged.plot(column='_growth2014_15', cmap='RdGy', legend=True)
    plt.title("Indian States GDP for 2014-15")
    plt.savefig(fname="GSDP_growth_14_15.jpg")
    plt.show()  # it clears the figure after creation therefore savefig should be used before show.
    return

# Test the func  1 here



# func 2: Interactivemap (Dashboard)
# Sample state-wise data with coordinates (approximation for demonstration)
data_with_coords = {
    "state_uts": ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh"],
    "growth2021_22": [18.47, 14.81, 13.89, 12.85, 11.84],
    "latitude": [15.9129, 28.2170, 26.2006, 25.0961, 21.2787],
    "longitude": [79.7400, 94.7278, 92.9376, 85.3131, 81.8661],
}

# Create a DataFrame
geo_df = pd.DataFrame(data_with_coords)

# Create a Folium map
map_center = [20.5937, 78.9629]  # Center of India (approximate)
interactive_map = folium.Map(location=map_center, zoom_start=5, tiles="CartoDB positron")

# Add markers for each state with growth data
for _, row in geo_df.iterrows():
    growth = row["growth2021_22"]
    color = "green" if growth and growth > 15 else "orange" if growth else "gray"
    popup_text = f"<b>{row['state_uts']}</b><br>Growth (2021-22): {growth if growth else 'NA'}%"
    folium.CircleMarker(
        location=(row["latitude"], row["longitude"]),
        radius=10 if growth else 5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=200),
    ).add_to(interactive_map)

# Save and display the map
interactive_map.save("./interactive_map.html")






"""
Next Project:
Geovisualization is done!
in the next analysis india states shape file should be adjusted according to new states
cntnd.. Interactive map visuaization should be fitted to our data and inside a function.
"""