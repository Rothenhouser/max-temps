from src.data import get_linked_urls, DATA_DIR_URL


def test_get_linked_urls():
    data_urls = get_linked_urls(DATA_DIR_URL, "zip")
    assert (
        data_urls[0]
        == "https://opendata.dwd.de/climate_environment/CDC/observations_germany/"
        "climate/monthly/kl/historical/monatswerte_KL_00001_19310101_19860630_hist.zip"
    )
