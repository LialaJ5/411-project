import pytest

from boxing.models.boxers_model import Boxers

# --- Fixtures ---

@pytest.fixture
def boxer_ali(session):
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

def test_create_boxer(session):
    """Test creating a new boxer."""
    Boxers.create_boxer("Alberta", lat=36.86, lon=-112.62)
    boxer = session.query(Boxers).filter_by(name="Alberta").first()
    assert boxer is not None


def test_create_boxer_duplicate_name(session, boxer_ali):
    """Test creating a boxer with a duplicate name."""
    with pytest.raises(ValueError, match="already exists"):
        Boxers.create_boxer("Boston",52.97, -0.02)

