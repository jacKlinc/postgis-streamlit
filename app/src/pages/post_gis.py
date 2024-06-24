import streamlit as st
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import folium
from streamlit_folium import st_folium

from ..utils import plot_coords
from ..types import Page


engine = create_engine("postgresql://username:password@localhost:5432/your_database")


def get_store_buffers():
    query = """
    SELECT id, ST_Buffer(geom, 5000) AS geom
    FROM stores;
    """
    return gpd.read_postgis(query, engine, geom_col="geom")


def get_demographic_overlay():
    query = """
    SELECT p.id, p.name, d.population_density
    FROM potential_locations p
    JOIN demographics d ON ST_Contains(d.geom, p.geom)
    WHERE d.population_density > 1000;
    """
    return gpd.read_postgis(query, engine, geom_col="geom")

def display_map(buffer_distance):
    store_buffers = get_store_buffers()
    m = folium.Map(location=[latitude, longitude], zoom_start=12)

    for _, row in store_buffers.iterrows():
        folium.GeoJson(row['geom']).add_to(m)
    
    st_folium(m, width=700, height=500)



class PostGIS(Page):
    def write(self):
        st.title("Post GIS")
        
        st.sidebar.header("Options")
        buffer_distance = st.sidebar.slider("Buffer Distance (meters)", 1000, 10000, 5000)
        
        display_map(buffer_distance)

