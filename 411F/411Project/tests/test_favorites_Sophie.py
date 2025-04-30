import time

import pytest

#from boxing.models.ring_model import RingModel
#from boxing.models.boxers_model import Boxers

from weatherFolder.models.favorites_model import FavoritesModel
from weatherFolder.models.cities_model import Cities
from unittest.mock import patch, MagicMock

# CHANGE (finish)
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
    # now we need to not only create the boxer but also add it to the database
    # and commit the session to persist the changes
    session.add(city)
    session.commit()
    return city

# CHANGE (Finish)
def test_clear_favorites(favorites_model):
    """Test that clear_favorites empties the favorites.

    """
    favorites_model.favorites = [1, 2]  # Assuming boxer IDs 1 and 2 are in the favorites)

    favorites_model.clear_favorites()

    assert len(favorites_model.favorites) == 0, "Favorites should be empty after calling clear_favorites."

#CHANGE (Finish)
def test_clear_favorite_empty(favorites_model, caplog):
    """Test that calling clear_favorite on an empty favorites logs a warning and keeps the favorites empty.

    """
    with caplog.at_level("WARNING"):
        favorites_model.clear_favorites()

    assert len(favorites_model.favorites) == 0, "Favorites should remain empty if it was already empty."

    assert "Attempted to clear an empty favorites." in caplog.text, "Expected a warning when clearing an empty Favorites."

# CHANGE (Finish)
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

# CHANGE (Finish)
def test_get_forecast_city_not_in_favorites(favorites_model):
    """Test that get_forecast_city raises ValueError if city_id is not in favorites."""

    favorites_model.favorites = []  # Empty favorites list

    with pytest.raises(ValueError, match="City ID 1 is not in favorites."):
        favorites_model.get_forecast_city(1)
