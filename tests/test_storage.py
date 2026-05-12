from src.measurement import DaylightMeasurement
from src.storage import load_measurements, save_measurements


def test_save_and_load_measurements(tmp_path, monkeypatch):
    import src.storage as storage

    test_file = tmp_path / "saved_measurements.json"
    # Redirect the storage module to a temporary file for the test run.
    monkeypatch.setattr(storage, "STORAGE_FILE", test_file)

    measurements = [
        DaylightMeasurement(
            date="16-04-26",
            location_name="Grua",
            day_length="13:45:00",
            sunrise="06:12:00",
            sunset="19:57:00",
        ),
        DaylightMeasurement(
            date="17-04-26",
            location_name="Grua",
            day_length="13:50:00",
            sunrise="06:09:00",
            sunset="20:01:00",
        ),
    ]

    save_measurements(measurements)
    loaded = load_measurements()

    assert len(loaded) == 2
    assert loaded[0].date == "16-04-26"
    assert loaded[1].date == "17-04-26"
