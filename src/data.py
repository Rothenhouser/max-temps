import pandas as pd
import requests

DATA_DIR_URL = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/monthly/kl/historical/"
STATION_INFO = DATA_DIR_URL + "/KL_Monatswerte_Beschreibung_Stationen.txt"


def get_station_info():
    # Can't parse the headers along with the rest, add manually
    return pd.read_fwf(
        STATION_INFO,
        encoding="windows-1252",
        colspecs="infer",
        infer_nrows=10,
        skiprows=[0, 1],
        header=None,
        names=[
            "Stations_id",
            "von_datum",
            "bis_datum",
            "Stationshoehe",
            "geoBreite",
            "geoLaenge",
            "Stationsname",
            "Bundesland",
        ],
    )


import requests
from bs4 import BeautifulSoup


def get_linked_urls(parent_url, ext=""):
    response = requests.get(parent_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return [
        parent_url + href
        for node in soup.find_all("a")
        if (href := node.get("href")).endswith(ext)
    ]


url = DATA_DIR_URL
ext = "zip"
data_urls = get_linked_urls(url, ext)

import re


def parse_data_urls(data_urls):
    availability = {}
    for url in data_urls:
        m = re.search("KL_(\d*)_(\d*)_(\d*)_hist", url)
        stn_id, start, end = map(int, m.groups())
        if stn_id in availability:
            raise ValueError(f"Parsed more than one URL for {stn_id}")
        availability[stn_id] = {"start": start, "end": end, "url": url}
    return availability


def filter_availability(availability, latest_start=19800000, earliest_end=20200000):
    availability_df = pd.DataFrame(parse_data_urls(data_urls)).T.reset_index(
        names="station_id"
    )
    useful_stations = availability_df[
        (availability_df["end"] >= earliest_end)
        & (availability_df["start"] <= latest_start)
    ]
    print(
        f"Of {len(data_urls)} data files, only {len(useful_stations)} are long enough to be interesting."
    )
    return useful_stations


actual_data_availability = pd.DataFrame(parse_data_urls(data_urls)).T.reset_index(
    names="station_id"
)
actual_data_availability.head()
