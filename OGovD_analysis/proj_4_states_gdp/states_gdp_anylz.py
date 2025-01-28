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

def get_GDP_interactive_map(api_url):
    """
    This function creates a interactive GSDP visualization for various states in India
    Parameters
    api_url: URL of the API
    """
    params = {
        "api-key": API_INFO["api_key"],
        "format": "json",
        "limit": 10000
    }
    response = requests.get(api_url, params)
    data = response.json()
    # Create a DataFrame
    gdp_df = pd.DataFrame(data["records"])
    geo_sample_df = pd.DataFrame.from_dict(geo_coordinates,
                                           orient='index',
                                           columns=["latitude", "longitude"]).reset_index()
    geo_sample_df.rename(columns={'index': 'States'}, inplace=True)
    geo_df = gdp_df.merge(geo_sample_df,
                             how="left",
                             left_on="state_uts",
                             right_on="States")
    geo_df["_growth2021_22"] = pd.to_numeric(geo_df["_growth2021_22"], errors='coerce').fillna(8)
    geo_df = geo_df.dropna(subset=["latitude", "longitude"])
    # Create a Folium map
    map_center = [20.5937, 78.9629]  # Center of India (approximate)
    interactive_map = folium.Map(location=map_center, zoom_start=5, tiles="CartoDB positron")

    # Add markers for each state with growth data
    for _, row in geo_df.iterrows():
        growth = row["_growth2021_22"]
        color = "green" if growth and growth > 15 else "orange" if growth and growth > 10 else "red"
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
    return

# test func2 here
gsdp_url = "https://api.data.gov.in/resource/adb4b1da-159f-46b3-a9c0-0545fe9ddda0?"





"""
Next Project:
Geovisualization is done!
in the next visualizatio india states shape file should be adjusted according to new states
cntnd.. Test the 2nd function visualization and validate the data itseems that more nulls values in it!
"""