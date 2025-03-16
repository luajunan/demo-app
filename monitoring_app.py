import streamlit as st
import requests
import pandas as pd
import altair as alt

# from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import time

# _ = st_autorefresh(interval=60000, limit=1000, key="refresh")

# FastAPI endpoint (update the URL as needed)
API_URL = "http://localhost:8000/metrics"

# Initialize the session start time if not set
if "init_time" not in st.session_state:
    st.session_state.init_time = datetime.now()

# Check if 3 days have passed since the session was initialized
if datetime.now() - st.session_state.init_time > timedelta(days=3):
    st.session_state.clear()  # This will clear all session state variables

# Initialize data storage in session_state if not already present
if "metrics_data" not in st.session_state:
    st.session_state.metrics_data = pd.DataFrame(
        columns=["timestamp", "pending_tasks", "completed_tasks"]
    )


def fetch_metrics():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        # Ensure that the new data includes required keys
        if "pending_tasks" in data and "completed_tasks" in data:
            data["timestamp"] = datetime.now()
            return data
        else:
            st.error("Invalid data format received from API")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching metrics: {e}")
        return None


def main():
    st.title("Task Queue Metrics Dashboard")
    # refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 60, 10)
    minutes = 10
    refresh_interval = minutes * 60

    # Create placeholders for data and chart
    table_placeholder = st.empty()
    chart_placeholder = st.empty()

    # Polling loop
    while True:
        metrics = fetch_metrics()
        if metrics:
            # Create a new DataFrame row for the latest metrics
            new_row = pd.DataFrame([metrics])
            # Convert 'timestamp' to datetime if needed
            new_row["timestamp"] = pd.to_datetime(new_row["timestamp"])
            new_row = new_row.dropna(axis=1, how="all")
            # Append new data using pd.concat()
            st.session_state.metrics_data = pd.concat(
                [st.session_state.metrics_data, new_row], ignore_index=True
            )

            # Optional: display the latest 10 rows in a table
            table_placeholder.write(st.session_state.metrics_data.tail(10))

            # Prepare data for plotting
            # Melt the DataFrame to have columns: timestamp, Metric, Count
            # Ensure that 'pending_tasks' and 'completed_tasks' are numeric
            df_plot = st.session_state.metrics_data.copy()
            df_plot["pending_tasks"] = pd.to_numeric(
                df_plot["pending_tasks"], errors="coerce"
            )
            df_plot["completed_tasks"] = pd.to_numeric(
                df_plot["completed_tasks"], errors="coerce"
            )

            # Filter to only include data from the last 3 months
            three_months_ago = pd.Timestamp.now() - pd.DateOffset(months=3)
            df_plot = df_plot[df_plot["timestamp"] >= three_months_ago]

            df_daily = (
                df_plot.set_index("timestamp")
                .resample(f"{minutes}min")
                .mean()
                .reset_index()
            )

            chart_data = df_daily.melt(
                "timestamp", var_name="Metric", value_name="Count"
            )

            # Build Altair line chart
            chart = (
                alt.Chart(chart_data)
                .mark_line(point=True)
                .encode(
                    x=alt.X(
                        "timestamp:T",
                        title="Timestamp",
                        axis=alt.Axis(format="%Y-%m-%d %H:%M"),
                    ),
                    y=alt.Y("Count:Q", title="Count"),
                    color="Metric:N",
                )
                .properties(width=700, height=400, title="Task Metrics Over Time")
            )

            chart_placeholder.altair_chart(chart, use_container_width=True)
        else:
            st.write("No new metrics fetched.")

        time.sleep(refresh_interval)


if __name__ == "__main__":
    main()
