from __future__ import annotations

import pandas as pd
import streamlit as st

from storage import load_measurements


def load_dashboard_data() -> tuple[list, pd.DataFrame]:
    """Load saved measurements and convert them to a DataFrame for dashboard use."""

    # Leser alle lagrede målinger fra JSON.
    measurements = load_measurements()

    if not measurements:
        return measurements, pd.DataFrame()

    # Gjør DaylightMeasurement-objektene om til dictionaries,
    # slik at pandas og Streamlit kan bruke dem.
    measurement_data = [measurement.to_dict() for measurement in measurements]
    df = pd.DataFrame(measurement_data)

    # Konverterer dato fra tekst til datetime for riktig sortering og plotting.
    df["date"] = pd.to_datetime(df["date"])

    # Konverterer HH:MM:SS-strenger til tallverdier for grafer.
    df["day_length_hours"] = pd.to_timedelta(df["day_length"]).dt.total_seconds() / 3600
    df["daily_increase_minutes"] = pd.to_timedelta(df["daily_increase"]).dt.total_seconds() / 60

    return measurements, df


def render_header(measurement_count: int) -> None:
    """Render the dashboard title and short intro text."""

    st.title("Daylight Dashboard")
    st.write("A dashboard for daylight and seasonal development.")
    st.caption(f"Loaded {measurement_count} measurements")


def render_latest_metrics(latest_measurement) -> None:
    """Render metric cards for the latest saved daylight measurement."""

    st.subheader(f"Latest measurement — {latest_measurement.location_name}")
    st.caption(latest_measurement.date)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Day length", latest_measurement.day_length)

    with col2:
        st.metric("Sunrise", latest_measurement.sunrise)

    with col3:
        st.metric("Sunset", latest_measurement.sunset)

    col4, col5 = st.columns(2)

    with col4:
        st.metric("Daily increase", latest_measurement.daily_increase)

    with col5:
        st.metric("Total increase", latest_measurement.total_increase)


def render_charts(df: pd.DataFrame) -> None:
    """Render dashboard charts for daylight development."""

    st.divider()
    st.subheader("Day length over time")

    st.subheader("Light development per day.")
    
    st.write("Day length measured in hours: ")
    
    st.line_chart(
        df,
        x="date",
        y="day_length_hours",
    )

    st.write("Daily increase measured in minutes.")

    st.bar_chart(
        df,
        x="date",
        y="daily_increase_minutes",
    )


def render_history_table(df: pd.DataFrame) -> None:
    """Render the saved measurements as a table."""  
    
    st.divider()
    st.subheader("Saved measurements")
    
    # Lager en egen Dataframe for visningen, slik at data i graf ikke blir brukt videre.
    display_df = df.copy()
    
    #Dato og klokkeslett:
    display_df["date"] = display_df["date"].dt.date
    
    #Kolonner som er relevante for brukeren.
    visible_columns = [
        "date",
        "location_name",
        "day_length",
        "sunrise",
        "sunset",
        "daily_increase",
        "total_increase",
    ]
    
    display_df = display_df[visible_columns]

    # Gir kolonnene mer lesbare navn i dashboardet.
    display_df = display_df.rename(
        columns={
            "date": "Date",
            "location_name": "Location",
            "day_length": "Day length",
            "sunrise": "Sunrise",
            "sunset": "Sunset",
            "daily_increase": "Daily increase",
            "total_increase": "Total increase",
        }
    )

    st.dataframe(df[visible_columns], use_container_width=True)


def main() -> None:
    """Run the Streamlit dashboard."""

    st.set_page_config(
        page_title="Daylight Dashboard",
        page_icon="☀️",
        layout="wide",
    )

    measurements, df = load_dashboard_data()

    if not measurements:
        st.title("Daylight Dashboard")
        st.warning("No saved measurements found. Run `python -m src.main --save --location Grua` first.")
        return


    #Siste målingen som blir brukt til nøkkeltallene øverst.
    latest_measurement = measurements[-1]

    render_header(len(measurements))
    render_latest_metrics(latest_measurement)
    render_charts(df)
    render_history_table(df)


if __name__ == "__main__":
    main()