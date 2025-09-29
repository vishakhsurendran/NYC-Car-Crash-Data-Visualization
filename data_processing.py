import requests
import pandas as pd
import streamlit as st
from datetime import datetime

BASE_URL = "https://data.cityofnewyork.us/resource/h9gi-nx95.json"

INCIDENT_COLUMNS = {
    "Injured": "number_of_persons_injured",
    "Killed": "number_of_persons_killed",
}

def build_where(years):
    conditions = []
    for year in years:
        start = f"{year}-01-01T00:00:00"
        end = f"{year}-12-31T23:59:59"
        conditions.append(f"(crash_date between '{start}' and '{end}')")
    return " OR ".join(conditions)

def build_query(years, incidents, limit=5000, offset=0):
    select_parts = ["borough", "crash_date", "latitude", "longitude"]
    for incident in incidents:
        col = INCIDENT_COLUMNS[incident]
        select_parts.append(col)

    select = ", ".join(select_parts)
    where = build_where(years)

    query = (
        f"?$select={select}"
        f"&$where={where}"
        f"&$limit={limit}&$offset={offset}"
    )
    return BASE_URL + query

@st.cache_data(show_spinner=False, ttl=3600)
def get_crash_data(years, incidents):
    all_data = []
    offset = 0
    limit = 5000

    while True:
        url = build_query(years, incidents, limit=limit, offset=offset)
        response = requests.get(url)

        if response.status_code != 200:
            st.error(f"Failed to fetch data: {response.status_code} -> {response.text}")
            raise RuntimeError(f"Failed to fetch data: {response.status_code} -> {response.text}")

        batch = response.json()
        if not batch:
            break

        all_data.extend(batch)
        if len(batch) < limit:
            break
        offset += limit

    if not all_data:
        return pd.DataFrame()

    crash_data = pd.DataFrame(all_data)
    crash_data["borough"] = crash_data["borough"].fillna("Unknown")

    # Convert crash_date
    crash_data["crash_date"] = pd.to_datetime(crash_data["crash_date"], errors="coerce")

    # Convert numeric fields
    for incident in incidents:
        col = INCIDENT_COLUMNS[incident]
        out_col = incident.lower()
        crash_data[out_col] = pd.to_numeric(crash_data[col], errors="coerce").fillna(0)

    return crash_data
