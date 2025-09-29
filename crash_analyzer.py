import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def plot_stacked_bar(df, incidents):
    agg = df.groupby("borough")[[i.lower() for i in incidents]].sum().reset_index()
    fig = px.bar(
        agg,
        x="borough",
        y=[i.lower() for i in incidents],
        title="Crashes by Borough",
        barmode="stack",
        labels={"value": "Count", "borough": "Borough", "variable": "Incident Type"},
        color_discrete_map={"injured": "crimson", "killed": "steelblue"},
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_trends(df, incidents):
    df["year"] = df["crash_date"].dt.year
    agg = df.groupby("year")[[i.lower() for i in incidents]].sum().reset_index()

    fig = go.Figure()
    for incident in incidents:
        fig.add_trace(
            go.Scatter(
                x=agg["year"],
                y=agg[incident.lower()],
                mode="lines+markers",
                name=incident,
            )
        )

    fig.update_layout(
        title="Trends Over Time",
        xaxis_title="Year",
        yaxis_title="Count",
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_map(df):
    # Remove missing coordinates
    df = df.dropna(subset=["latitude", "longitude"])
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    st.map(df[["latitude", "longitude"]])
