import time

import pytest

#from boxing.models.ring_model import RingModel
#from boxing.models.boxers_model import Boxers

from weatherFolder.models.favorites_model import FavoritesModel
from weatherFolder.models.cities_model import Cities

@pytest.fixture
def favorites_model():
    """Fixture to provide a new instance of RingModel for each test.

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

def test_add_to_favorite(favorites_model, sample_city1):
    """Test that a boxer is correctly added to the ring.

    """
    favorites_model.add_to_favorite(sample_city1.id)  # Assuming boxer with ID 1 is "Muhammad Ali"

    assert len(favorites_model.favorites) == 1, "Favorites should contain one city after calling add_to_favorite."
    assert favorites_model.favorites[0]== 1, "Expected 'Boston' in the favorite."

def test_add_to_favorite(favorites_model):
    """Test that enter_ring raises an error when the ring is full.

    """
    favorites_model.favorites = [1, 2]

    with pytest.raises(RuntimeError):
        favorites_model.add_to_favorite(3)

    assert len(favorites_model.favorites) == 2, "Favorites should still contain only the two cities."



def test_get_weather_city(favorites_model, sample_city1):
    """Test the get_fighting_skill method.

    """
    expected_score_1 = "clear sky"
    assert favorites_model.get_weather_city(sample_city1.id) == expected_score_1, f"Expected score: {expected_score_1}"

def test_get_weather_city(favorites_model, sample_city1):
    """Test the get_fighting_skill method.

    """

    favorites_model.favorites = [1, 2]
    
    with pytest.raises(ValueError):
        favorites_model.get_weather_city(3)

    expected_score_1 = "clear sky"
    assert favorites_model.get_weather_city(sample_city1.id) == expected_score_1, f"Expected score: {expected_score_1}"