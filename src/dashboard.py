from __future__ import annotations
import streamlit as st

try:
    from .storage import get_latest_measurement, load_measurements
except ImportError:
    from storage import get_latest_measurement, load_measurements


def main() -> None:
    """Kjører streamlit dashboardet"""

    st.set_page_config(
        page_title="Daylight dashboard",
        page_icon="☀️",
        layout="wide",
    )

    st.title("Daylight Dashboard")
    st.write("Enkelt dashboard for dagslys og sesong endring.")

    # Leser inn siste lagrede måling fra JSON.
    # Data brukes for å representere en graf og historisk utvikling. 
    measurements = load_measurements()
    
    if not measurements:
        st.warning("Ingen lagret data er funnet. kjør `python -m src.main --save`. først")
        return
    
    latest_measurement = measurements[-1]

    st.subheader(f"Sist måling - {latest_measurement.location_name}")
    st.caption(f"Loaded {len(measurements)} measurements")
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


if __name__ == "__main__":
    main()
