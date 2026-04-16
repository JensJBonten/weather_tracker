# værprosjekt

Small Python project for analyzing how daylight changes over time from an Excel sheet.

## What the project does

The script reads the workbook in `data/`, normalizes the Norwegian column names, converts Excel date/time values into proper pandas types, and prints a short summary of:

- the date range in the dataset
- day length at the start and end of the period
- sunrise and sunset development
- total and largest daily increase in daylight

It can also save a chart as a PNG file.

## Project structure

- `src/main.py` contains the CLI entry point
- `src/data_loader.py` reads and normalizes the Excel data
- `src/reporting.py` formats summaries and terminal previews
- `src/plotting.py` creates the PNG chart
- `data/Dagens lengde (2).xlsx` is the current source dataset
- `requirements.txt` lists the Python dependencies

## Setup

Create and activate a virtual environment, then install the dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

Run the analysis:

```bash
python -m src.main
```

If you are using the checked-in Windows virtual environment:

```powershell
.\venv\Scripts\python.exe -m src.main
```

Preview fewer or more rows:

```bash
python -m src.main --preview 3
```

Save a plot:

```bash
python -m src.main --plot output/daylight.png
```

Use a different Excel file:

```bash
python -m src.main --file data/my_other_file.xlsx
```

## Storage helpers

The project also includes a small JSON storage layer in `src/storage.py` for
persisting `DaylightMeasurement` objects to `data/saved_measurements.json`.

## Tests

Run the storage test suite from the repository root:

```bash
pytest
```

## Expected Excel columns

The script currently expects these exact source columns:

- `Dato`
- `Lengde`
- `Sol opp`
- `Sol Ned`
- `Dagens lengeøkning\ni min, per sist målt dato`
- `Total økning siden start\nav måling pr/min:`

If the workbook changes, update `NORMALIZED_COLUMNS` in `src/data_loader.py`.

## Notes about Excel time values

Excel stores time values in a few different ways, and `pandas` may read them differently depending on platform and cell formatting.

This script now handles:

- Excel fractional day numbers
- text values that can be parsed as durations
- `datetime.time` values that often appear on Windows

If you still get parsing errors, inspect the raw column values in the workbook first and then adjust `to_excel_timedelta()` in `src/data_loader.py`.

## Improvements worth doing next

- Move the current exploratory script into a package with separate modules for loading, validation, and plotting.
- Add tests for the column mapping and date/time conversions.
- Rename the Excel file to something simpler and stable, without spaces or `(2)`.
- Keep the virtual environment out of the repository and recreate it from `requirements.txt`.
- Add automatic export of cleaned data to CSV so the analysis becomes easier to reuse.
