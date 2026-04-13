from __future__ import annotations

import argparse
from datetime import datetime, time, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
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


def parse_args() -> argparse.Namespace:
    """Parse command-line options for the daylight analysis script."""
    parser = argparse.ArgumentParser(
        description="Analyze daylight development from the Excel file in data/."
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=DATA_FILE,
        help=f"Path to the Excel file. Default: {DATA_FILE}",
    )
    parser.add_argument(
        "--preview",
        type=int,
        default=5,
        help="Number of rows to print as a preview. Use 0 to disable.",
    )
    parser.add_argument(
        "--plot",
        type=Path,
        help="Optional output path for a PNG chart.",
    )
    return parser.parse_args()


def load_daylight_data(file_path: Path) -> pd.DataFrame:
    """Load the Excel file and normalize the columns used by the project."""
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find Excel file: {file_path}")

    df = pd.read_excel(file_path)
    missing_columns = [column for column in NORMALIZED_COLUMNS if column not in df.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Excel file is missing expected columns: {missing}")

    df = df.rename(columns=NORMALIZED_COLUMNS).copy()
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%y")

    # Excel time cells may be read as fractional days, strings, or datetime.time
    # objects depending on platform and workbook formatting.
    for column in ("day_length", "sunrise", "sunset", "daily_increase", "total_increase"):
        df[column] = df[column].map(to_excel_timedelta)

    return df.sort_values("date").reset_index(drop=True)


def to_excel_timedelta(value: object) -> pd.Timedelta:
    """Convert one Excel-style time value into a pandas Timedelta."""
    if pd.isna(value):
        return pd.NaT

    if isinstance(value, pd.Timedelta):
        return value

    if isinstance(value, timedelta):
        return pd.Timedelta(value)

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
        stripped = value.strip()
        try:
            numeric_value = float(stripped.replace(",", "."))
        except ValueError:
            return pd.to_timedelta(stripped)
        return pd.to_timedelta(numeric_value, unit="D")

    raise TypeError(f"Unsupported Excel time value: {value!r} ({type(value)!r})")


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


def save_plot(df: pd.DataFrame, output_path: Path) -> None:
    """Save a simple chart showing total day length and daily increase."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    axes[0].plot(df["date"], df["day_length"].dt.total_seconds() / 3600, linewidth=2)
    axes[0].set_title("Day Length Over Time")
    axes[0].set_ylabel("Hours")
    axes[0].grid(alpha=0.3)

    axes[1].bar(df["date"], df["daily_increase"].dt.total_seconds() / 60, width=1.5)
    axes[1].set_title("Daily Increase")
    axes[1].set_ylabel("Minutes")
    axes[1].grid(alpha=0.3)

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    """Run the CLI workflow."""
    args = parse_args()
    df = load_daylight_data(args.file)

    print("Daylight dataset summary")
    for line in build_summary(df):
        print(f"- {line}")

    print_preview(df, args.preview)

    if args.plot:
        save_plot(df, args.plot)
        print(f"\nSaved plot to {args.plot}")


if __name__ == "__main__":
    main()
