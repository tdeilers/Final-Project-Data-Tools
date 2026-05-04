import streamlit as st
import requests
import json
import time
import datetime
import pandas as pd
import plotly.express as px

payload2 = 	{"seriesid":[    "CES0000000001",  # Nonfarm employment
    "LNS14000000",    # Unemployment rate
    "LNS11300000",    # Labor force participation 
    "LNS12300000",    # Employment-pop ratio
    "CES3000000001",  # Manufacturing
    "CES7000000001",  # Leisure & hospitality
    "CES0500000003",  # Avg hourly earnings
]}
def fetch_data(url,payload):
    success = False
    while success is False:
        try:
            response = requests.post(url, json = payload)
            if response.status_code == 200:
                success = True
        except:
            time.sleep(5)

            print("Error... Retryign")
    return response.json()

datatext = fetch_data("https://api.bls.gov/publicAPI/v2/timeseries/data", payload2)

rows = []
print(type(datatext))
#for now, this seems to just be giving me nonfarm data but that works with me. lets see streamlit 
for series in datatext["Results"]["series"]:
    series_id = series["seriesID"]

    for item in series["data"]:
        rows.append({
            "series_id": series_id,
            "year": item["year"],
            "period": item["period"],
            "period_name": item["periodName"],
            "value": item["value"],
        })
df = pd.DataFrame(rows)
df["value"] = pd.to_numeric(df["value"],errors = "coerce")
df["month"] = df["period"].str.replace("M", "", regex=False)
df["date"] = pd.to_datetime(df["year"] + "-" + df["month"] + "-01")

df.to_csv("masterdata.csv")