
import streamlit as st
import pandas as pd
from datetime import datetime

from api.f1_api import (
    get_race_details,
    get_session_drivers
)

from api.f1_api import (
    get_race_details,
    get_session_drivers,
    get_session_laps,
    get_race_results
)

# Page configuration
st.set_page_config(
    page_title="Formula 1 Race Analytics Dashboard",
    page_icon="🏎️",
    layout="wide"
)

# Dashboard heading
st.title("🏎️ Formula 1 Race Analytics Dashboard")
st.markdown(
    "Explore historical Formula 1 races, drivers and race statistics."
)

st.divider()

# Sidebar
st.sidebar.header("Race Selection")

year = st.sidebar.selectbox(
    "Select Season",
    [2026,2025, 2024, 2023],
    index=0
)

# Fetch race information
@st.cache_data(ttl=3600)
def load_races(selected_year):
    return get_race_details(selected_year)

races = load_races(year)

if not races:
    st.error("No race data available for this season.")
    st.stop()

race_names = [race["race_name"] for race in races]

selected_race_name = st.sidebar.selectbox(
    "Select Grand Prix",
    race_names
)

selected_race = next(
    race for race in races
    if race["race_name"] == selected_race_name
)

# Race overview
st.header(selected_race["race_name"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Season", year)
col2.metric("Country", selected_race["country"])
col3.metric("Circuit", selected_race["circuit"])
col4.metric("Session", selected_race["session"])

st.write("**Race Date:**", selected_race["date"])


# Race Results
st.divider()
st.header("🏆 Official Race Results")

@st.cache_data(ttl=3600)
def load_race_results(year, race_name):
    return get_race_results(year, race_name)

results = load_race_results(
    year,
    selected_race["race_name"]
)

if results:
    results_df = pd.DataFrame([
        {
            "Position": result.get("position"),
            "Driver": (
                result["Driver"]["givenName"] + " " +
                result["Driver"]["familyName"]
            ),
            "Code": result["Driver"].get("code"),
            "Team": result.get("Constructor", {}).get("name", "N/A"),
            "Grid": result.get("grid"),
            "Laps": result.get("laps"),
            "Points": result.get("points"),
            "Status": result.get("status"),
            "Time": result.get("Time", {}).get("time", "N/A"),
            "Fastest Lap": result.get("FastestLap", {})
                .get("Time", {}).get("time", "N/A")
        }
        for result in results
    ])

    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True
    )

    # Race winner
    winner = results_df.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Race Winner", winner["Driver"])
    col2.metric("Winning Team", winner["Team"])
    col3.metric("Points", winner["Points"])

else:
    st.info(
        "Official race results are not available yet. "
        "Results will appear after the race classification is published."
    )


# Driver information
st.subheader("🏁 Participating Drivers")

@st.cache_data(ttl=3600)
def load_drivers(session_key):
    return get_session_drivers(session_key)

drivers = load_drivers(selected_race["session_key"])

if drivers:
    driver_df = pd.DataFrame(drivers)

    display_columns = [
        column for column in [
            "driver_number",
            "full_name",
            "name_acronym",
            "team_name",
            "country_code"
        ]
        if column in driver_df.columns
    ]

    st.dataframe(
        driver_df[display_columns],
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("No driver information available.")
