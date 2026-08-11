import requests
import pandas as pd


def get_navision_data(url, username, password):

    response = requests.get(
        url,
        auth=(username, password),
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return pd.DataFrame(data["value"])