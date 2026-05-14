from dataclasses import dataclass


@dataclass
class DaylightMeasurement:
    """Datamodell for en dagslysmåling på ett sted og én dato."""

    # Alle feltene lagres som strenger for at objektet enkelt skal kunne skrives til JSON.
    date: str
    location_name: str
    day_length: str
    sunrise: str
    sunset: str
    daily_increase: str
    total_increase: str

    def to_dict(self) -> dict:
        # Gjør målingen om til en dictionary som kan lagres som JSON.
        return {
            "date": self.date,
            "location_name": self.location_name,
            "day_length": self.day_length,
            "sunrise": self.sunrise,
            "sunset": self.sunset,
            "daily_increase": self.daily_increase,
            "total_increase": self.total_increase
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DaylightMeasurement":
        #Bygger et DaylightMeasurement-objekt fra data som er lest fra JSON.
        return cls(
            date=data["date"],
            location_name=data["location_name"],
            day_length=data["day_length"],
            sunrise=data["sunrise"],
            sunset=data["sunset"],
            daily_increase=data["daily_increase"],
            total_increase=data["total_increase"]
        )
