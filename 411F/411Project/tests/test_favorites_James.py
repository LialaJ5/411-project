import pytest
from weatherFolder.models.favorites_model import FavoritesModel
from weatherFolder.models.cities_model import Cities
from unittest.mock import patch, MagicMock

@pytest.fixture
def favorites_model():
    """Fixture to provide a new instance of FavoritesModel for each test.

    """
    return FavoritesModel()

@pytest.fixture
def sample_city1(session):
    city = Cities(
        id = 4930956,
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
        id = 3165523,
        name="Province of Turin",
        lat=45.133,
        lon=7.367,
    )
    session.add(city)
    session.commit()
    return city

@pytest.fixture
def sample_cities(session):
    cities = [sample_city1,sample_city2]
    return cities

def sample_cities_empty(session):
    cities = []
    session.add(cities)
    session.commit()
    return cities


# was test_get_boxers_empty
def test_get_cities_empty(favorites_model):
    """Test that get_boxers returns an empty list when there are no boxers and logs a warning.

    """
    #favorites_model = sample_cities_empty
    #with caplog.at_level("WARNING"):
    #    cities = favorites_model.get_all_cities_and_weather()
    favorites_model.favorites = []

    assert favorites_model.get_all_cities_and_weather() == [], "Expected get_boxers to return an empty list when there are no boxers."

    #assert "Retrieving boxers from an empty ring." in caplog.text, "Expected a warning when getting boxers from an empty ring."

# test_get_boxers_with_data
def test_get_cities_with_data(app, favorites_model, sample_cities):
    """Test that get_boxers returns the correct list when there are boxers.

    # Note that app is a fixture defined in the conftest.py file

    """
    #favorites_model.ring.extend([boxer.id for boxer in sample_boxers])

    city1 = Cities(name="TestCity", lat=10.0, lon=20.0)
    city1.id = 1

    city2 = Cities(name="TestCity2", lat=20.0, lon=40.0)
    city2.id = 2

    favorites_model.favorites = [1,2]
    assert favorites_model.get_all_cities_and_weather() == [("TestCity", "broken clouds" ),("TestCity2", "broken clouds")], "Expected get_boxers to return the correct boxers list."