import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

SERIES_MAP = {
    "CES0000000001": "Nonfarm Employment",
    "LNS14000000": "Unemployment Rate",
    "LNS11300000": "Labor Force Participation Rate",
    "LNS12300000": "Employment-Population Ratio",
    "CES3000000001": "Manufacturing Employment",
    "CES7000000001": "Leisure and Hospitality Employment",
    "CES0500000003": "Average Hourly Earnings",
}

DATA_PATH = Path("data/master_data.csv")
BLS_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


def fetch_bls_data():
    current_year = datetime.now().year

    payload = {
        "seriesid": list(SERIES_MAP.keys()),
        "startyear": str(current_year - 1),
        "endyear": str(current_year),
    }

    response = requests.post(BLS_URL, json=payload)
    response.raise_for_status()

    return response.json()


def bls_json_to_dataframe(data):
    rows = []

    for series in data["Results"]["series"]:
        series_id = series["seriesID"]

        for item in series["data"]:
            rows.append({
                "series_id": series_id,
                "series_name": SERIES_MAP.get(series_id, series_id),
                "year": item["year"],
                "period": item["period"],
                "period_name": item["periodName"],
                "value": item["value"],
                "latest": item.get("latest", "false"),
            })

    df = pd.DataFrame(rows)

    df["month"] = df["period"].str.replace("M", "", regex=False)
    df["date"] = pd.to_datetime(df["year"] + "-" + df["month"] + "-01")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.drop(columns=["month"])

    return df


def update_master_data(new_df):
    if DATA_PATH.exists():
        old_df = pd.read_csv(DATA_PATH)
        old_df["date"] = pd.to_datetime(old_df["date"])

        combined = pd.concat([old_df, new_df], ignore_index=True)
    else:
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
    new_df = bls_json_to_dataframe(data)
    updated_df = update_master_data(new_df)

    print("BLS data updated successfully.")
    print(f"Rows saved: {len(updated_df)}")
    print(f"Latest date: {updated_df['date'].max().date()}")


if __name__ == "__main__":
    main()