from __future__ import annotations

import pandas as pd


def format_duration(value: pd.Timedelta) -> str:
    """Format a Timedelta as HH:MM:SS for readable terminal output."""
    if pd.isna(value):
        return "N/A"

    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def build_summary(df: pd.DataFrame) -> list[str]:
    """Build a compact summary for the loaded dataset."""
    first_row = df.iloc[0]
    last_row = df.iloc[-1]

    return [
        f"Rows: {len(df)}",
        f"Date range: {first_row['date'].date()} -> {last_row['date'].date()}",
        f"Day length: {format_duration(first_row['day_length'])} -> {format_duration(last_row['day_length'])}",
        f"Sunrise: {format_duration(first_row['sunrise'])} -> {format_duration(last_row['sunrise'])}",
        f"Sunset: {format_duration(first_row['sunset'])} -> {format_duration(last_row['sunset'])}",
        f"Total increase: {format_duration(last_row['total_increase'])}",
        f"Largest daily increase: {format_duration(df['daily_increase'].max())}",
    ]


def print_preview(df: pd.DataFrame, rows: int) -> None:
    """Print the first rows in a readable, formatted table."""
    if rows <= 0:
        return

    preview = df.head(rows).copy()
    for column in ("day_length", "sunrise", "sunset", "daily_increase", "total_increase"):
        preview[column] = preview[column].map(format_duration)

    print("\nPreview:")
    print(preview.to_string(index=False))
