from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__:
    from .data_loader import DATA_FILE, load_daylight_data
    from .measurement_mapper import measurements_from_dataframe
    from .plotting import save_plot
    from .reporting import build_summary, print_preview
    from .storage import get_latest_measurement, save_measurements
else:
    sys.path.append(str(Path(__file__).resolve().parent))
    from data_loader import DATA_FILE, load_daylight_data
    from measurement_mapper import measurements_from_dataframe
    from plotting import save_plot
    from reporting import build_summary, print_preview
    from storage import save_measurements, get_latest_measurement


def parse_args() -> argparse.Namespace:
    """Leser inn valg som brukeren kan sende inn fra kommandolinjen."""
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
    parser.add_argument(
        "--location",
        type=str,
        default="Grua",
        help="Location name for the daylight measurements, Default: Grua.",
    )
    return parser.parse_args()


def main() -> None:
    """Kjører hele arbeidsflyten fra Excel-fil til utskrift, lagring og valgfri graf."""
    args = parse_args()

    # Leser Excel-filen og normaliserer kolonnenavn og tidsverdier.
    df = load_daylight_data(args.file)

    # Skriver en kort oppsummering av datasettet i terminalen.
    print("Daylight dataset summary")
    for line in build_summary(df):
        print(f"- {line}")

    # Viser de første radene, med mindre brukeren har valgt --preview 0.
    print_preview(df, args.preview)

    # Konverterer dataframet til målbare objekter.
    # Dette kobler data-loader-delen av prosjektet med lagringsdelen.
    # Endrer hardkodet måleområdet til å bruke kommandolinjen i stedet.
    # Kan bruke Excel/API-flyt senere for flere steder.
    measurements = measurements_from_dataframe(df, location_name=args.location)

    # Lagrer målingene til data/saved_measurements.json.
    # Denne arbeidsflyten kan senere bli benyttet for API.
    save_measurements(measurements)

    # Laster den sist lagrede målingen tilbake fra fil for å teste at lagringen fungerer.
    latest_measurement = get_latest_measurement()

    if latest_measurement:
        print("\nLatest saved measurement:")
        print(f"- Date: {latest_measurement.date}")
        print(f"- Location: {latest_measurement.location_name}")
        print(f"- Day length: {latest_measurement.day_length}")
        print(f"- Sunrise: {latest_measurement.sunrise}")
        print(f"- Sunset: {latest_measurement.sunset}")
        print(f"- Daily increase: {latest_measurement.daily_increase}")
        print(f"- Total increase: {latest_measurement.total_increase}")
        

    if args.plot:
        # Lager en PNG-graf bare når brukeren sender inn --plot.
        save_plot(df, args.plot)
        print(f"\nSaved plot to {args.plot}")


if __name__ == "__main__":
    main()
