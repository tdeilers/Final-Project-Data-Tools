import streamlit
import requests
import json
import time
import datetime
import pandas as pd

payload2 = 	{"seriesid":["LAUCN040010000000005", "LAUCN040010000000006", "OEUN000000056--5747213213"]}
def fetch_data(url,payload):
    success = False
    while success is False:
        try:
            response = requests.get(url, json = payload)
            if response.status_code == 200:
                success = True
        except:
            time.sleep(5)

            print("Error... Retryign")
    return response.text
print("yo")
print(fetch_data("https://api.bls.gov/publicAPI/v2/timeseries/popular", payload2))
print("yo yo")