import streamlit as st
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
import folium
from streamlit_folium import st_folium
from psycopg2 import OperationalError

from ..utils import plot_coords
from ..types import Page


engine = create_engine("postgresql://jack:password@localhost:5432/test_db")


def get_store_buffers():
    query = """
    SELECT *
    FROM LondonWard;
    """
    try:
        return gpd.read_postgis(query, engine, geom_col="geom")
    except OperationalError as e:
        st.error(f"Authentication error, {e}")


def display_map(buffer_distance):
    store_buffers = get_store_buffers()
    latitude = 51.5074  # Example: Center of London
    longitude = -0.1278
    
    st.write(store_buffers) 

    m = folium.Map(location=[latitude, longitude], zoom_start=12)

    for _, row in store_buffers.iterrows():
        folium.GeoJson(row["geom"]).add_to(m)

    st_folium(m, width=700, height=500)


class PostGIS(Page):
    def write(self):
        st.title("Post GIS")

        st.sidebar.header("Options")
        buffer_distance = st.sidebar.slider(
            "Buffer Distance (meters)", 1000, 10000, 5000
        )

        display_map(buffer_distance)
