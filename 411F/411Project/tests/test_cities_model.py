#key : boxing = weatherFolder \ boxer_model = cities_model \ Boxers = Cities \

import pytest

from weatherFolder.models.cities_model import Cities

# --- Fixtures ---

@pytest.fixture
def city_Boston(session):
    """Fixture for Muhammad Ali."""
    boxer = Boxers(name="Boston", lat=52.97, lon=-0.02)
    session.add(boxer)
    session.commit()
    return boxer

"""
@pytest.fixture
def boxer_tyson(session):
    boxer = Boxers(name="Mike Tyson", weight=220, height=178, reach=71, age=35)
    session.add(boxer)
    session.commit()
    return boxer

"""

# --- Create Boxer ---

def test_create_city(session):
    """Test creating a new city."""
    CIties.create_city("Alberta", lat=36.86, lon=-112.62)
    city = session.query(Cities).filter_by(name="Alberta").first()
    assert city is not None


def test_create_city_duplicate_name(session, boxer_ali):
    """Test creating a boxer with a duplicate name."""
    with pytest.raises(ValueError, match="already exists"):
        Boxers.create_boxer("Boston",52.97, -0.02)

