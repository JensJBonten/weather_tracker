from dataclasses import dataclass


@dataclass
class DaylightMeasurement:
    """Serializable daylight measurement for one location on one date."""

    date: str
    location_name: str
    day_length: str
    sunrise: str
    sunset: str

    def to_dict(self) -> dict:
        """Convert the measurement to a JSON-friendly dictionary."""
        return {
            "date": self.date,
            "location_name": self.location_name,
            "day_length": self.day_length,
            "sunrise": self.sunrise,
            "sunset": self.sunset,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DaylightMeasurement":
        """Create a measurement instance from stored dictionary data."""
        return cls(
            date=data["date"],
            location_name=data["location_name"],
            day_length=data["day_length"],
            sunrise=data["sunrise"],
            sunset=data["sunset"],
        )
