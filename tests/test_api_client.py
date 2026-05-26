from src.api_client import get_default_location, describe_api_goal


def test_get_default_location_returns_grua():
    """Check that the API client has a default location."""

    location = get_default_location()

    assert location.name == "Grua"
    assert isinstance(location.latitude, float)
    assert isinstance(location.longitude, float)


def test_describe_api_goal_returns_expected_steps():
    """Check that the API integration goal is documented in code."""

    api_goal = describe_api_goal()

    assert "Convert API response into DaylightMeasurement objects" in api_goal
    assert "Store API measurements in SQLite with source='api'" in api_goal