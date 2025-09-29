import streamlit as st
import data_processing
import crash_analyzer

st.set_page_config(page_title="NYC Car Crash Data Visualization", page_icon=":car:", layout="wide")

st.title("🚦 NYC Car Crash Data Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
incidents = st.sidebar.multiselect(
    "Select Incident Type(s)", ["Injured", "Killed"], ["Injured", "Killed"]
)
years = st.sidebar.multiselect(
    "Select Year(s)", list(range(2015, 2026)), [2025]
)
boroughs = st.sidebar.multiselect(
    "Select Borough(s)", ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"], []
)

if not incidents or not years:
    st.error("Please select at least one incident type and one year.")
else:
    with st.spinner("Fetching crash data..."):
        crashes = data_processing.get_crash_data(years, incidents)

    if crashes.empty:
        st.warning("No data returned for the selected filters.")
    else:
        if boroughs:
            crashes = crashes[crashes["borough"].isin(boroughs)]

        # Key Metrics
        st.subheader("Key Metrics")
        col1, col2 = st.columns(2)
        if "Injured" in incidents:
            col1.metric("Total Injured", int(crashes["injured"].sum()))
        if "Killed" in incidents:
            col2.metric("Total Killed", int(crashes["killed"].sum()))

        # Visuals
        st.subheader("📊 Crashes by Borough")
        crash_analyzer.plot_stacked_bar(crashes, incidents)

        st.subheader("📈 Trends Over Time")
        crash_analyzer.plot_trends(crashes, incidents)

        if "latitude" in crashes and "longitude" in crashes:
            st.subheader("🗺️ Crash Locations")
            crash_analyzer.plot_map(crashes)

        # Raw data toggle
        if st.sidebar.checkbox("Show Raw Data"):
            st.write(crashes)
