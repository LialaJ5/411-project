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
def sample_boxer1(session):
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

def test_add_to_favorite(favorites_model, sample_boxer1):
    """Test that a boxer is correctly added to the ring.

    """
    favorites_model.add_to_favorite(sample_boxer1.id)  # Assuming boxer with ID 1 is "Muhammad Ali"

    assert len(favorites_model.favorites) == 1, "Ring should contain one boxer after calling enter_ring."
    assert favorites_model.favorites[0]== 1, "Expected 'Muhammad Ali' (id 1) in the ring."



def test_get_weather_city(favorites_model, sample_boxer1):
    """Test the get_fighting_skill method.

    """
    expected_score_1 = "clear sky"
    assert favorites_model.get_weather_city(sample_boxer1.id) == expected_score_1, f"Expected score: {expected_score_1}"