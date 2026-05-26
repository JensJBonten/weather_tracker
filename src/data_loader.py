from __future__ import annotations

from datetime import datetime, time, timedelta
from pathlib import Path

import pandas as pd

DATA_FILE = Path("data") / "Dagens lengde (2).xlsx"
NORMALIZED_COLUMNS = {
    "Dato": "date",
    "Lengde": "day_length",
    "Sol opp": "sunrise",
    "Sol Ned": "sunset",
    "Dagens lengeøkning\ni min, per sist målt dato": "daily_increase",
    "Total økning siden start\nav måling pr/min:": "total_increase",
}


def load_daylight_data(file_path: Path) -> pd.DataFrame:
    """Laster Excel-filen og normaliserer kolonnene prosjektet bruker."""
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find Excel file: {file_path}")

    # Leser hele regnearket før vi sjekker at de forventede kolonnene finnes.
    daylight_dataframe = pd.read_excel(file_path)
    missing_columns = [
        column for column in NORMALIZED_COLUMNS if column not in daylight_dataframe.columns
    ]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Excel file is missing expected columns: {missing}")

    # Gir kolonnene engelske interne navn, slik at resten av koden slipper Excel-tekstene.
    daylight_dataframe = daylight_dataframe.rename(columns=NORMALIZED_COLUMNS).copy()
    daylight_dataframe["date"] = pd.to_datetime(daylight_dataframe["date"], format="%d.%m.%y")

    # Excel-tid kan bli lest som desimaltall, tekst, datetime eller time.
    # Derfor sendes alle tidskolonnene gjennom samme konverteringsfunksjon.
    for column in ("day_length", "sunrise", "sunset", "daily_increase", "total_increase"):
        daylight_dataframe[column] = daylight_dataframe[column].map(to_excel_timedelta)

    # Sorterer på dato slik at oppsummering, graf og "siste måling" får riktig rekkefølge.
    return daylight_dataframe.sort_values("date").reset_index(drop=True)


def to_excel_timedelta(value: object) -> pd.Timedelta:
    """Konverterer én Excel-lignende tidsverdi til pandas Timedelta."""
    if pd.isna(value):
        return pd.NaT

    # Verdier som allerede er tidsdifferanser kan brukes direkte eller pakkes inn av pandas.
    if isinstance(value, pd.Timedelta):
        return value

    if isinstance(value, timedelta):
        return pd.Timedelta(value)

    # datetime og time inneholder klokkeslett, så vi henter ut timer, minutter og sekunder.
    if isinstance(value, datetime):
        return pd.Timedelta(
            hours=value.hour,
            minutes=value.minute,
            seconds=value.second,
            microseconds=value.microsecond,
        )

    if isinstance(value, time):
        return pd.Timedelta(
            hours=value.hour,
            minutes=value.minute,
            seconds=value.second,
            microseconds=value.microsecond,
        )

    if isinstance(value, (int, float)):
        return pd.to_timedelta(value, unit="D")

    if isinstance(value, str):
        # Tekst kan enten være et tall med komma/desimalpunkt eller en vanlig tidsstreng.
        stripped = value.strip()
        try:
            numeric_value = float(stripped.replace(",", "."))
        except ValueError:
            return pd.to_timedelta(stripped)
        return pd.to_timedelta(numeric_value, unit="D")

    # Hvis Excel-filen inneholder en ukjent type, feiler vi tydelig i stedet for å gjette.
    raise TypeError(f"Unsupported Excel time value: {value!r} ({type(value)!r})")
