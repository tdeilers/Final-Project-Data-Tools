import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

payload2 = 	{"seriesid":[    "CES0000000001",   # Nonfarm employment
    "LNS14000000",     # Unemployment rate
    "LNS11300000",     # Labor force  participation 
    "LNS12300000",     # Employment-pop   ratio
    "CES3000000001",   # Man ufacturing
    "CES7000000001",    # Leisure & hospitality
    "CES0500000003",   # Avg horly earnings
]}

DATA_PATH = Path("masterdata.csv")



def fetch_bls_data():
    #gets last year of data
    current_year = datetime.now().year

    payload = {
        "seriesid": payload2["seriesid"],
        "startyear": str(current_year - 1),
        "endyear": str(current_year),
    }

    response = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", json=payload)
    response.raise_for_status()

    return response.json()

#so this
def jsontodataframe(data):
    rows = []

    for series in data["Results"]["series"]:
        series_id = series["seriesID"]

        for item in series["data"]:
            rows.append({
                "series_id": series_id,
                "year": item["year"],
                "period": item["period"],
                
                "value": item["value"],
            })

    df = pd.DataFrame(rows)
    #convert shit to month
    df["month"] = df["period"].str.replace("M", "", regex=False)
    df["date"] = pd.to_datetime(df["year"] + "-" + df["month"] + "-01")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.drop(columns=["month","period","year"])

    return df


def updatemasterdata(new_df):
    #get data old one 
    if DATA_PATH.exists():
        old_df = pd.read_csv(DATA_PATH)


        old_df["date"] = pd.to_datetime(old_df["date"])

        combined = pd.concat([old_df, new_df], ignore_index=True)
    else:
        #easier then two things., files, that is
        combined = new_df

    combined = combined.drop_duplicates(
        subset=["series_id", "date"],
        keep="last"
    )

    combined = combined.sort_values(["series_id", "date"])

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(DATA_PATH, index=False)

    return combined


def main():
    data = fetch_bls_data()
    new_df = jsontodataframe(data)
    updated_df = updatemasterdata(new_df)

 


if __name__ == "__main__":
    main()