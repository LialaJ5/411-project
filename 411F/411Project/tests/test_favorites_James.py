import pytest
from tests.James_favorites import FavoritesModel
from tests.James_favorites import Cities

@pytest.fixture
def favorites_model():
    """Fixture to provide a new instance of RingModel for each test.

    """
    return FavoritesModel()

# was test_get_boxers_empty
def test_get_cities_empty(favorites_model, caplog):
    """Test that get_boxers returns an empty list when there are no boxers and logs a warning.

    """
    with caplog.at_level("WARNING"):
        cities = favorites_model.get_all_cities_and_weather()

    assert cities == [], "Expected get_boxers to return an empty list when there are no boxers."

    assert "Retrieving boxers from an empty ring." in caplog.text, "Expected a warning when getting boxers from an empty ring."

# test_get_boxers_with_data
def test_get_cities_with_data(app, favorites_model, sample_cities):
    """Test that get_boxers returns the correct list when there are boxers.

    # Note that app is a fixture defined in the conftest.py file

    """
    #favorites_model.ring.extend([boxer.id for boxer in sample_boxers])

    boxers = favorites_model.get_boxers()
    assert boxers == sample_cities, "Expected get_boxers to return the correct boxers list."