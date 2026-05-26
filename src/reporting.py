from __future__ import annotations

import pandas as pd


def format_duration(value: pd.Timedelta) -> str:
    """Formaterer en Timedelta som HH:MM:SS for lesbar terminalutskrift."""
    if pd.isna(value):
        return "N/A"

    # Gjør tiden om til hele sekunder før den deles opp i timer, minutter og sekunder.
    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def build_summary(daylight_dataframe: pd.DataFrame) -> list[str]:
    """Bygger en kort oppsummering av det innlastede datasettet."""
    # Første og siste rad viser utviklingen gjennom hele måleperioden.
    first_measurement_row = daylight_dataframe.iloc[0]
    last_measurement_row = daylight_dataframe.iloc[-1]

    return [
        f"Rows: {len(daylight_dataframe)}",
        f"Date range: {first_measurement_row['date'].date()} -> {last_measurement_row['date'].date()}",
        f"Day length: {format_duration(first_measurement_row['day_length'])} -> {format_duration(last_measurement_row['day_length'])}",
        f"Sunrise: {format_duration(first_measurement_row['sunrise'])} -> {format_duration(last_measurement_row['sunrise'])}",
        f"Sunset: {format_duration(first_measurement_row['sunset'])} -> {format_duration(last_measurement_row['sunset'])}",
        f"Total increase: {format_duration(last_measurement_row['total_increase'])}",
        f"Largest daily increase: {format_duration(daylight_dataframe['daily_increase'].max())}",
    ]


def print_preview(daylight_dataframe: pd.DataFrame, row_count: int) -> None:
    """Skriver ut de første radene som en lesbar og formatert tabell."""
    if row_count <= 0:
        return

    # Kopierer preview-radene slik at vi kan formatere visningen uten å endre originaldataene.
    preview_dataframe = daylight_dataframe.head(row_count).copy()
    for column in ("day_length", "sunrise", "sunset", "daily_increase", "total_increase"):
        preview_dataframe[column] = preview_dataframe[column].map(format_duration)

    print("\nPreview:")
    print(preview_dataframe.to_string(index=False))
