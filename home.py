import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium import Marker
from streamlit_folium import st_folium
import warnings 
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Persian Restaurants",
    page_icon=":world_map:",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv('data/restaurants.csv')
    return df

# Read the restaurant data from a CSV file
restaurants = load_data()


# Convert the restaurant data to a GeoDataFrame
restaurants_gpd = gpd.GeoDataFrame(
    restaurants, geometry=gpd.points_from_xy(restaurants.Longitude, restaurants.Latitude))

# Set the coordinate reference system (CRS) to EPSG 4326 (WGS84)
restaurants_gpd.crs = 'epsg:4326'
#st.write(restaurants_gpd.head())

left, right = st.columns(2)

with left:
    # Create a base map
    st.caption("Select a place on map for details:")
    m = folium.Map(location=[43.77125215639117, -79.41965130523319], zoom_start=10)

    # Your code here: Add a marker for each Berkeley location
    for idx, row in restaurants_gpd[restaurants_gpd["Country"]=="Canada"].iterrows():
        Marker([row['Latitude'], row['Longitude']], popup=row['Name'] ,tooltip=row['Name']).add_to(m)

    # call to render Folium map in Streamlit
    st_data = st_folium(m, width=725)

with right:
    if st_data["last_object_clicked_popup"]:
        restaurant_name = st_data["last_object_clicked_popup"]
        st.header(restaurant_name)
        poped_restaurant = restaurants.loc[restaurants["Name"]==restaurant_name].squeeze()
        st.write("Phone Number: ", poped_restaurant["Phone"])
        st.write("Address: ", poped_restaurant["Address"])
        st.write("Website: ", poped_restaurant["Website"])
    else:
        pass