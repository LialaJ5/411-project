import time

import pytest

from weatherFolder.models.favorites_model import FavoritesModel
from weatherFolder.models.cities_model import Cities
from unittest.mock import patch, MagicMock

@pytest.fixture
def favorites_model():
    """Fixture to provide a new instance of FavoritesModel for each test.

    """
    return FavoritesModel()

# Fixtures providing sample boxers
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

#was sample_boxers
@pytest.fixture
def sample_cities(session):
    cities = [sample_city1,sample_city2]
    return cities

def sample_cities_empty(session):
    cities = []
    session.add(cities)
    session.commit()
    return cities


##########################################################
# City and Favorites
##########################################################

def test_clear_favorites(favorites_model):
    """Test that clear_favorites empties the favorites.

    """
    favorites_model.favorites = [1, 2]  # Assuming boxer IDs 1 and 2 are in the favorites)

    favorites_model.clear_favorites()

    assert len(favorites_model.favorites) == 0, "Favorites should be empty after calling clear_favorites."

def test_clear_favorite_empty(favorites_model, caplog):
    """Test that calling clear_favorite on an empty favorites logs a warning and keeps the favorites empty.

    """
    with caplog.at_level("WARNING"):
        favorites_model.clear_favorites()

    assert len(favorites_model.favorites) == 0, "Favorites should remain empty if it was already empty."

    assert "Attempted to clear an empty favorites." in caplog.text, "Expected a warning when clearing an empty Favorites."

def test_get_cities_empty(favorites_model):
    """Test that get_cities returns an empty list when there are no city and logs a warning.

    """
    favorites_model.favorites = []
    assert favorites_model.get_all_cities_and_weather() == [], "Expected get_cities to return an empty list when there are no cities."

@patch("weatherFolder.models.cities_model.Cities.get_city_by_id")
@patch("requests.get")
@patch("os.getenv", return_value="fake-key")
def test_get_cities_with_data(mock_getenv, mock_requests_get, mock_get_city_by_id, favorites_model, sample_city1, sample_city2):
    """Test that get_all_cities_and_weather returns the correct (city, weather) tuples."""

    favorites_model.favorites = [sample_city1.id, sample_city2.id]

    mock_get_city_by_id.side_effect = [sample_city1, sample_city2]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "weather": [{"description": "broken clouds"}]
    }
    mock_requests_get.return_value = mock_response

    result = favorites_model.get_all_cities_and_weather()

    expected = [
        (sample_city1, "broken clouds"),
        (sample_city2, "broken clouds")
    ]

    assert [(c.name, w) for c, w in result] == [(c.name, w) for c, w in expected], "Expected correct cities and weather"

def test_add_to_favorite(favorites_model, sample_city1):
    """Test that a city is correctly added to the favorites.

    """
    favorites_model.add_to_favorite(sample_city1.id)  # Assuming boxer with ID 1 is "Muhammad Ali"

    assert len(favorites_model.favorites) == 1, "Favorites should contain one city after calling add_to_favorite."
    assert favorites_model.favorites[0]== 1, "Expected 'Boston' in the favorite."

def test_add_to_favorite_full(favorites_model):
    """Test that add_to_favorite raises an error when the favorites is full.

    """
    favorites_model.favorites = [1, 2]

    with pytest.raises(RuntimeError):
        favorites_model.add_to_favorite(3)

    assert len(favorites_model.favorites) == 2, "Favorites should still contain only the two cities."

@patch("requests.get") 
def test_get_weather_city(mock_get, favorites_model, sample_city1):
    """Test that get_weather_city returns mocked weather description."""
    favorites_model.favorites = [sample_city1.id]

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "weather": [{"description": "overcast clouds"}]
    }
    mock_get.return_value = mock_response

    expected = "overcast clouds"
    result = favorites_model.get_weather_city(sample_city1.id)
    assert result == expected

def test_get_weather_city_error(favorites_model, sample_city1):
    """Test that get_weather_city raises ValueError for invalid ID and returns a valid string for a valid city."""
    favorites_model.favorites = [1, 2]

    with pytest.raises(ValueError):
        favorites_model.get_weather_city(9999)

    result = favorites_model.get_weather_city(sample_city1.id)
    assert isinstance(result, str)
    assert len(result) > 0

def test_get_forecast_city_success(favorites_model):
    """Test that get_forecast_city returns valid forecast for a favorite city."""

    city = Cities(name="TestCity", lat=10.0, lon=20.0)
    city.id = 1
    favorites_model.favorites = [1]

    with patch("weatherFolder.models.cities_model.Cities.get_city_by_id", return_value=city), \
         patch("requests.get") as mock_get, \
         patch("os.getenv", return_value="fake-key"):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "list": [
                {
                    "dt_txt": "2025-04-30 12:00:00",
                    "main": {"temp_max": 25, "temp_min": 15},
                    "pop": 0.1,
                    "weather": [{"description": "clear sky"}]
                }
            ]
        }
        mock_get.return_value = mock_response

        result = favorites_model.get_forecast_city(1)

        assert result["city"] == "TestCity", "City name should match."
        assert len(result["forecast"]) == 1, "Forecast list should contain one entry."
        assert result["forecast"][0]["condition"] == "clear sky", "Forecast condition should match mock."

def test_get_forecast_city_not_in_favorites(favorites_model):
    """Test that get_forecast_city raises ValueError if city_id is not in favorites."""

    favorites_model.favorites = []  # Empty favorites list

    with pytest.raises(ValueError, match="City ID 1 is not in favorites."):
        favorites_model.get_forecast_city(1)
