from src.measurement import DaylightMeasurement
from src.storage import load_measurements, save_measurements


def test_save_and_load_measurements(tmp_path, monkeypatch):
    import src.storage as storage

    test_file = tmp_path / "saved_measurements.json"
    # Sender lagringsmodulen til en midlertidig fil slik at testen ikke endrer ekte data.
    monkeypatch.setattr(storage, "STORAGE_FILE", test_file)

    # Lager to eksempel-målinger som skal lagres og leses tilbake.
    measurements = [
        DaylightMeasurement(
            date="16-04-26",
            location_name="Grua",
            day_length="13:45:00",
            sunrise="06:12:00",
            sunset="19:57:00",
            daily_increase="00:05:00",
            total_increase="04:08:00",
        ),
        DaylightMeasurement(
            date="17-04-26",
            location_name="Grua",
            day_length="13:50:00",
            sunrise="06:09:00",
            sunset="20:01:00",
            daily_increase="00:05:00",
            total_increase="04:13:00",
        ),
    ]

    # Sjekker at lagring og innlasting beholder både antall og datoverdier.
    save_measurements(measurements)
    loaded_measurements = load_measurements()

    assert len(loaded_measurements) == 2
    assert loaded_measurements[0].date == "16-04-26"
    assert loaded_measurements[1].date == "17-04-26"
    assert loaded_measurements[0].daily_increase == "00:05:00"
    assert loaded_measurements[0].total_increase == "04:08:00"
    assert loaded_measurements[1].daily_increase == "00:05:00"
    assert loaded_measurements[1].total_increase == "04:13:00"
