from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .data_loader import DATA_FILE, load_daylight_data
    from .plotting import save_plot
    from .reporting import build_summary, print_preview
except ImportError:
    from data_loader import DATA_FILE, load_daylight_data
    from plotting import save_plot
    from reporting import build_summary, print_preview


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

    if args.plot:
        save_plot(df, args.plot)
        print(f"\nSaved plot to {args.plot}")


if __name__ == "__main__":
    main()
