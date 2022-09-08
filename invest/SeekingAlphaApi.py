import requests
import os
from time import sleep


class SeekingAlphaApi:

    def __init__(self):
        self.baseurl = "https://seeking-alpha.p.rapidapi.com"
        self.headers = {
            # Fetch the API key from the environment variable
            'X-RapidAPI-Key': os.environ['SEEKING_ALPHA_API_KEY'],
            'x-rapidapi-host': "seeking-alpha.p.rapidapi.com"
        }
        print(self.headers)

    def get_historical_chart(self, symbol, timeline="MAX", attempts=0):
        querystring = {"symbol": symbol, "period": timeline}

        url = f"{self.baseurl}/symbols/get-chart"

        response = requests.request("GET", url, headers=self.headers, params=querystring)
        if not response.json() or response.json()["attributes"] == {} or response.status_code != 200:
            if attempts < 2:
                print(f"Failed to fetch chart data for {symbol}. "
                      f"Trying again. after a sleep for {4 * 2 ** attempts} seconds")
                sleep(1 * 2 ** attempts)
                return self.get_historical_chart(symbol, timeline, attempts + 1)
            else:
                print(f"Failed to fetch chart data for {symbol}. Giving up.")
                return {}
        return response.json()
