"""
the idea to conduct descriptive as well as Geo-visualization for Indian states/AP district wise population data

Dataset: get from this Kagglehub link # Download latest version
path = https://www.data.gov.in/resource/state-wise-population-decadal-population-growth-rate-and-population-density-2011-0
"""
import pandas as pd
import folium
import geopandas as gpd
from folium.plugins import HeatMap

df = pd.read_csv("Table_2A_State_Uts.csv")
print(df.head())
# sorting the values alphabetically
df.sort_values(by=["India/State/Union Territory"],
               inplace=True,
               ignore_index=True)

# Load the shapefile (replace 'path_to_shapefile' with the actual path to your shapefile)
shapefile_path = './India Shape/india_ds.shp'
gdf = gpd.read_file(shapefile_path)


# Merge the GeoDataFrame with the DataFrame
merged = gdf.merge(df, left_on='STATE', right_on='India/State/Union Territory')

# Initialize the map centered on India
map_1 = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# type 1: Geovisualization Heatmap  of Indian population
heat_data = [
    [row['geometry'].centroid.y, row['geometry'].centroid.x, row['Population 2011']]
    for index, row in merged.iterrows()
]
HeatMap(heat_data).add_to(map_1)

# Save the map to an HTML file
map_1.save('india_population_heatmap.html')

# Optionally, display the map
map_1


# Initialize the map centered on India
map_2 = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

gdf.set_crs('EPSG:24378 ', inplace=True)
gdf = gdf.to_crs('EPSG:4326')

# Merge the GeoDataFrame with the DataFrame
merged_1 = gdf.merge(df, left_on='STATE', right_on='India/State/Union Territorys')
# Create a Choropleth map
folium.Choropleth(
    geo_data=merged_1,
    name='choropleth',
    data=df,
    columns=['India/State/Union Territory', 'Population 2011'],
    key_on='feature.properties.STATE',
    fill_color='BuPu',  # Color scheme (can be changed to others like 'YlGnBu', 'BuPu', etc.)
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total Population'
).add_to(map_2)

# Add a layer control
folium.LayerControl().add_to(map_2)

# Save the map to an HTML file
map_2.save('india_population_choropleth.html')

# Optionally, display the map
map_2


"""
Next steps:
Heatmap not genertaed after dataset change remove first row and then check X
"""

