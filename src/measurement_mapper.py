from __future__ import annotations

import pandas as pd

from .measurement import DaylightMeasurement
from .reporting import format_duration


def measurements_from_dataframe(
    df : pd.DataFrame, location_name: str,
) -> list[DaylightMeasurement]:
    """
    Genrerer rene daylight DataFrame rader til DaylightMeasurements objekter.
    
    """
    
    measurements: list[DaylightMeasurement] = []
    
    # Itererer over hver rad fra data_loader.py.
    # date har allerede blitt koverterert til datetime, og time kolonner er allerede blitt convertert til pandas Timedelta.
    
    for _, row in df.iterrows() : 
        measurement = DaylightMeasurement(
            # Data blir lagret her som ISO-string ettersom disse er "JSON-friendly" og lete å sammenligne samt sortere senere.
            date=row["date"].date().isoformat(), 
            
            # Beholder lokasjonen, slik at modellen i senere tid kan fungere med forskjellige lokasjoner. 
            location_name=location_name, 
            
            # Konverterer tidsdelta verdier til leselige strenger før de blir lagret. 
            
            day_length=format_duration(row["day_length"]),
            sunrise=format_duration(row["sunrise"]),
            sunset=format_duration(row["sunset"]),
        )
        
        measurements.append(measurement)
    return measurements
