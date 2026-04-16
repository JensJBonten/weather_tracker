from pathlib import Path
import json

try:
    from .measurement import DaylightMeasurement
except ImportError:
    from measurement import DaylightMeasurement

STORAGE_FILE = Path("data") / "saved_measurements.json"


def load_measurements() -> list[DaylightMeasurement]:
    """Load all saved measurements from disk."""
    if not STORAGE_FILE.exists():
        return []

    with open(STORAGE_FILE, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    return [DaylightMeasurement.from_dict(item) for item in raw_data]

def save_measurements(measurements: list[DaylightMeasurement]) -> None:
    """Write all measurements to disk as JSON."""
    STORAGE_FILE.parent.mkdir(parents=True, exist_ok=True)

    raw_data = [measurement.to_dict() for measurement in measurements]

    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(raw_data, file, indent=4)


def add_measurement(measurement: DaylightMeasurement) -> None:
    """Append one measurement to the stored collection."""
    measurements = load_measurements()
    measurements.append(measurement)
    save_measurements(measurements)


def get_latest_measurement() -> DaylightMeasurement | None:
    """Return the most recently saved measurement, if available."""
    measurements = load_measurements()
    if not measurements:
        return None
    return measurements[-1]

