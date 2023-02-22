from data import DATA_DIR_URL, _get_linked_file_urls, get_temperatures


def test_get_linked_file_urls():
    data_urls = _get_linked_file_urls(DATA_DIR_URL, "zip")
    assert (
        data_urls[0]
        == "https://opendata.dwd.de/climate_environment/CDC/observations_germany/"
        "climate/monthly/kl/historical/monatswerte_KL_00001_19310101_19860630_hist.zip"
    )


def test_get_temperatures():
    temps = get_temperatures(
        "https://opendata.dwd.de/climate_environment/CDC/observations_germany/"
        "climate/monthly/kl/historical/monatswerte_KL_00001_19310101_19860630_hist.zip"
    )
    assert len(temps) == 642
