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


def main() -> None:
    """Run the CLI workflow."""
    args = parse_args()
    df = load_daylight_data(args.file)

    print("Daylight dataset summary")
    for line in build_summary(df):
        print(f"- {line}")

    print_preview(df, args.preview)
    
    # Konverterer dataframet til et målbart objekt. 
    # Dette kobler "data-loader" av prosjektet med lagringsdelen. 
    
    measurements = measurements_from_dataframe(df, location_name="Grua")
    
    #Lagrer målingene til data/saved_measurement.json.
    #Denne arbeidsflyten kan senere bli benyttet for API. 
    
    save_measurements(measurements)
    
    #laster den sist lagrede målingen tilbake fra minnet for å teste om det fungerer. 
    latest_measurement = get_latest_measurement()
    
    if latest_measurement:
        print("\nLatest saved measurement:")
        print(f"- Date: {latest_measurement.date}")
        print(f"- Location: {latest_measurement.location_name}")
        print(f"- Day length: {latest_measurement.day_length}")
        print(f"- Sunrise: {latest_measurement.sunrise}")
        print(f"- Sunset: {latest_measurement.sunset}")

    if args.plot:
        save_plot(df, args.plot)
        print(f"\nSaved plot to {args.plot}")


if __name__ == "__main__":
    main()
