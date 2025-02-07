"""
the idea is to carry-out appropriate visualization preferably Geo-Visualization if no the other
Dataset (Gross State Domestic Product): https://www.data.gov.in/resource/gross-state-domestic-product-gsdp-current-prices-states-and-uts-2011-12-2021-22

NOTE: In the next Geo-Visualization india states shape file should be adjusted according to new states
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

    arguments:
    api_ur
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

def create_gdp_growth_map(api_endpoint, year):
    """
    Generates an interactive map showing GDP growth for Indian states.

    Parameters:
    - api_endpoint: takes the API end_point as Input.
    - year: The year in "YYYY_YY" format (e.g., "2021_22") to visualize growth.

    Returns:
    - A Folium map object.
    """
    params = {
        "api-key": API_INFO["api_key"],
        "format": "json",
        "limit": 10000
    }
    response = requests.get(api_endpoint, params)
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

    growth_col = f"_growth{year}"

    if growth_col not in geo_df.columns:
        raise ValueError(f"Column '{growth_col}' not found in data. Check the available columns.")

    # Ensure the growth column is numeric, replacing 'NA' or missing values with 8
    geo_df[growth_col] = pd.to_numeric(geo_df[growth_col], errors='coerce').fillna(8)

    # Drop rows with missing latitude or longitude to prevent mapping errors
    geo_df = geo_df.dropna(subset=["latitude", "longitude"])

    # Initialize Folium map centered on India
    interactive_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="CartoDB positron")

    # Add state markers with GDP growth info
    for _, row in geo_df.iterrows():
        growth = row[growth_col]
        color = "green" if growth and growth > 15 else "orange" if growth and growth > 10 else "red"
        popup_text = f"<b>{row['state_uts']}</b><br>Growth ({year}): {growth}%"

        folium.CircleMarker(
            location=(row["latitude"], row["longitude"]),
            radius=10 if growth > 8 else 5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=200),
        ).add_to(interactive_map)

    return geo_df, interactive_map


# test func2 here
gsdp_url = "https://api.data.gov.in/resource/adb4b1da-159f-46b3-a9c0-0545fe9ddda0?"

year_input = input(f"enter the desired year in the format as example '2021_21' ")
a, gdp_map = create_gdp_growth_map(gsdp_url, year_input)
gdp_map.save("gdp_growth_map.html")


"""
Next Project:
2nd Geovisualization is done!
Quick analyze the first 2two functions and start the 3rd type?? 
"""