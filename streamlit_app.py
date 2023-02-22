import plotly.express as px
import streamlit as st

from src.data import (
    get_station_info,
    get_temperatures,
    get_useful_stations_from_data_urls,
)


@st.cache_data()
def get_stations():
    return get_station_info()


# todo this is dumb
@st.cache_data()
def get_temps(url):
    return get_temperatures(url)


st.title("Development of max temperatures at German weather stations ")

data_load_state = st.text("Loading stations")

stations = get_stations()
st.write(stations)

useful_stations = get_useful_stations_from_data_urls()
st.write(
    f"Of {len(stations)} possible stations, only {len(useful_stations)} have current and long enough data."
)
st.write(useful_stations)

data_load_state.text("Loading stations... done")

useful_stations_merged = stations[
    stations["Stations_id"].isin(useful_stations["station_id"])
]

st.map(stations.rename(columns={"geoBreite": "latitude", "geoLaenge": "longitude"}))
st.map(
    useful_stations_merged.rename(
        columns={"geoBreite": "latitude", "geoLaenge": "longitude"}
    )
)

# todo multiselect, show name of station
# more challenging: select from map, colour map according to max temp rise
selected_station_id = st.selectbox("Choose a station ID", useful_stations["station_id"])


# todo clean data, -999 for missing value
temps = get_temps(
    useful_stations.query(f"station_id == {selected_station_id}")["url"].iloc[0]
)
annual_max = temps.resample("A").max()

st.plotly_chart(px.line(temps))
st.plotly_chart(px.line(annual_max))
