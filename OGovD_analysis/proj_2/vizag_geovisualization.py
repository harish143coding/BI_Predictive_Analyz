import folium
import geopandas as gpd

# Load the shapefile (replace 'andhra_pradesh_shapefile.shp' with the actual file path)
shapefile_path = "andhra_pradesh_administrative.shp"
data = gpd.read_file(shapefile_path)

# Inspect the data to identify columns for district and mandal names
print(data.head())

# Filter the data for Visakhapatnam district
visakhapatnam_data = data[data['NAME'] == 'Visakapatnam']  # Replace 'district_column_name' with the actual column name

# Ensure the GeoDataFrame is in WGS84 coordinate reference system (CRS)
visakhapatnam_data = visakhapatnam_data.to_crs(epsg=4326)

# Get the centroid of Visakhapatnam district to center the map
center = visakhapatnam_data.geometry.centroid.iloc[0].coords[0]

# Create a folium map centered on Visakhapatnam district
m = folium.Map(location=[center[1], center[0]], zoom_start=10, tiles='CartoDB positron')

# Add the mandal boundaries to the map
folium.GeoJson(
    visakhapatnam_data,
    name="Mandal Boundaries",
    style_function=lambda x: {
        'fillColor': 'blue',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    },
    tooltip=folium.features.GeoJsonTooltip(fields=['ADMIN_LEVE'], aliases=['Mandal:'])  # Replace 'mandal_column_name' with actual column name
).add_to(m)

# Add a layer control panel
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save("visakhapatnam_mandal_map.html")

# To display the map in Jupyter Notebook (if running in Jupyter)
# from IPython.display import IFrame
# IFrame("visakhapatnam_mandal_map.html", width=800, height=600)
