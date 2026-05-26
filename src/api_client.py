from __future__ import annotations
from dataclasses import dataclass


@dataclass
class ApiLocation: 
    """Data for området når jeg kaller på dagslys/vær data fra en API, blir trolig YR sin."""
    
    name: str
    latitude : float
    longitude : float
    

def get_default_location() -> ApiLocation: 
    """returnerer default lokasjonen som har blitt brukt i prosjektet, Grua i dette tilfelle."""
    
    return ApiLocation(
        name="Grua",
        latitude=60.257,
        longitude=10.662,
    )
    

def describe_api_goal() -> list[str]:
    """Beskrivelse på hva API integrasjonen skal gjøre i fremtiden. """
    return [
        "Fetch daylight or weather-related data for a location",
        "Convert API response into DaylightMeasurement objects",
        "Store API measurements in SQLite with source='api'",
        "Show API-backed measurements in the Streamlit dashboard",
    ]