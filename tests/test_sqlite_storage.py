from src.measurement import DaylightMeasurement
from src.sqlite_storage import (
    get_latest_measurement,
    initialize_database,
    load_measurements,
    save_measurements,
)


def test_save_and_load_measurements_from_sqlite(tmp_path):
    """Check that measurements can be saved to and loaded from SQLite."""

    database_file = tmp_path / "daylight.db"

    measurements = [
        DaylightMeasurement(
            date="2026-03-09",
            location_name="Grua",
            day_length="11:11:00",
            sunrise="06:52:00",
            sunset="18:04:00",
            daily_increase="00:16:00",
            total_increase="04:02:00",
        ),
        DaylightMeasurement(
            date="2026-03-10",
            location_name="Grua",
            day_length="11:17:00",
            sunrise="06:49:00",
            sunset="18:06:00",
            daily_increase="00:06:00",
            total_increase="04:08:00",
        ),
    ]

    initialize_database(database_file)
    save_measurements(measurements, database_file=database_file)

    loaded_measurements = load_measurements(database_file=database_file)
    latest_measurement = get_latest_measurement(database_file=database_file)

    assert len(loaded_measurements) == 2
    assert loaded_measurements[0].date == "2026-03-09"
    assert loaded_measurements[1].date == "2026-03-10"

    assert latest_measurement is not None
    assert latest_measurement.date == "2026-03-10"
    assert latest_measurement.location_name == "Grua"
    assert latest_measurement.total_increase == "04:08:00"
