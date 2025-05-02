#key : boxing = weatherFolder \ boxer_model = cities_model \ Boxers = Cities \

import pytest

from weatherFolder.models.cities_model import Cities
from unittest.mock import patch, MagicMock

# --- Fixtures ---

@pytest.fixture
def sample_city1(session):
    city = Cities(
        name="Boston",
        lat=52.97,
        lon=-0.02,
    )
    session.add(city)
    session.commit()
    return city

@pytest.fixture
def sample_city2(session):
    city = Cities(
        name="Province of Turin",
        lat=45.133,
        lon=7.367,
    )
    session.add(city)
    session.commit()
    return city

# --- Create City ---

def test_create_city_success(session):
    """Test creating a new city successfully."""
    Cities.create_city("Alberta", lat=36.86, lon=-112.62)
    city = session.query(Cities).filter_by(name="Alberta").first()
    assert city is not None
    assert city.name == "Alberta"
    assert city.lat == 36.86
    assert city.lon == -112.62


def test_create_city_duplicate_name(session):
    """Test creating a city with a duplicate name raises ValueError."""
    Cities.create_city("Boston", lat=40.0, lon=70.0)
    with pytest.raises(ValueError, match="already exists"):
        Cities.create_city("Boston", lat=50.0, lon=80.0)

# --- Get City by ID ---

def test_get_city_by_id(session):
    """Test retrieving a city by its ID successfully."""
    city = Cities(name="Chicago", lat=41.88, lon=-87.63)
    session.add(city)
    session.commit()

    retrieved = Cities.get_city_by_id(city.id)
    assert retrieved.name == "Chicago"
    assert retrieved.lat == 41.88
    assert retrieved.lon == -87.63


def test_get_city_by_id_error(app):
    """Test retrieving a city with an invalid ID raises ValueError."""
    with app.app_context():
        with pytest.raises(ValueError, match="not found"):
            Cities.get_city_by_id(99999)

# --- Get Weather ---

@patch("requests.get")
@patch("os.getenv", return_value="fake-api-key")
def test_get_weather(mock_getenv, mock_requests_get, session):
    """Test that get_weather returns the correct weather description when API succeeds."""
    city = Cities(name="Seattle", lat=47.61, lon=-122.33)
    session.add(city)
    session.commit()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "weather": [{"description": "light rain"}]
    }
    mock_requests_get.return_value = mock_response

    assert city.get_weather() == "light rain"

@patch("requests.get")
@patch("os.getenv", return_value="fake-api-key")
def test_get_weather_error(mock_getenv, mock_requests_get, session):
    """Test that get_weather raises an Exception if the API call fails."""
    city = Cities(name="Miami", lat=25.76, lon=-80.19)
    session.add(city)
    session.commit()

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_requests_get.return_value = mock_response

    with pytest.raises(Exception, match="Error with"):
        city.get_weather()