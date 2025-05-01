import logging
import math
import os
import time
from typing import List
import logging
from typing import List
import requests
import os
from dotenv import load_dotenv, dotenv_values

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

#from weatherFolder.db import db
#from weatherFolder.utils.logger import configure_logger

#from weatherFolder.models.cities_model import Cities
#from weatherFolder.utils.logger import configure_logger
#from weatherFolder.utils.api_utils import get_random
class FavoritesModel:
    """A class to manage the the ring in which boxers have fights.

    """

 #CHANGE
    def __init__(self):
        """Initializes the RingManager with an empty list of combatants.

        The ring is initially empty, and the boxer cache and time-to-live (TTL) caches are also initialized.
        The TTL is set to 60 seconds by default, but this can be overridden by setting the TTL_SECONDS environment variable.

        Attributes:
            ring (List[int]): The list of ids of the boxers in the ring.
            _boxer_cache (dict[int, Boxers]): A cache to store boxer objects for quick access.
            _ttl (dict[int, float]): A cache to store the time-to-live for each boxer.
            ttl_seconds (int): The time-to-live in seconds for the cached boxer objects.

        """
        """
        self.ring: List[int] = []
        self._boxer_cache: dict[int, Boxers] = {}
        self._ttl: dict[int, float] = {}
        self.ttl_seconds = int(os.getenv("TTL", 60))
        """

        self.favorites: List[int] = []
    def get_all_cities_and_weather(self): #-> List[str,str]:
        """Retrieves the current list of cities in the list.

        Returns:
            List[Cities]: A list of Cities dataclass instances representing the cities in the favorites list.

        """
        if not self.ring:
            logger.warning("Retrieving cities from an empty list.")
        else:
            logger.info(f"Retrieving {len(self.favorites)} cities from the list.")

        #now = time.time()
        cities: List[str,str] = []

        for city_id in self.favorites:
            #expired = city_id not in self._ttl or now > self._ttl[city_id]
            #if expired:
            #    logger.info(f"TTL expired or missing for boxer {city_id}. Refreshing from DB.")
            city = Cities.get_city_by_id(city_id)
            weather = Cities.getWeather(city_id)
            #    self._boxer_cache[city_id] = city
            #   self._ttl[city_id] = now + self.ttl_seconds
            #else:
            #    logger.debug(f"Using cached boxer {city_id} (TTL valid).")
            cities.append(city,weather)

        logger.info(f"Retrieved {len(cities)} boxers from the ring.")
        return cities

class Cities(db.Model):
    """Represents a competitive boxer in the system.

    This model maps to the 'boxers' table in the database and stores personal
    and performance-related attributes such as name, weight, height, reach,
    age, and fight statistics. Used in a Flask-SQLAlchemy application to
    manage boxer data, run simulations, and track fight outcomes.

    """
    """
    __tablename__ = 'boxers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    reach = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    fights = db.Column(db.Integer, nullable=False, default=0)
    wins = db.Column(db.Integer, nullable=False, default=0)
    weight_class = db.Column(db.String)
    """
    
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def __init__(self, name: str, lat: float, lon: float):
        """Initialize a new Boxer instance with basic attributes.

        Args:
            name (str): The boxer's name. Must be unique.
            weight (float): The boxer's weight in pounds. Must be at least 125.
            height (float): The boxer's height in inches. Must be greater than 0.
            reach (float): The boxer's reach in inches. Must be greater than 0.
            age (int): The boxer's age. Must be between 18 and 40, inclusive.

        Notes:
            - The boxer's weight class is automatically assigned based on weight.
            - Fight statistics (`fights` and `wins`) are initialized to 0 by default in the database schema.

        """
        self.name = name
        self.lat = lat
        self.lon = lon
    def get_city_by_id(cls, city_id: int) -> "Cities":
        """Retrieve a boxer by ID.

        Args:
            boxer_id: The ID of the boxer.

        Returns:
            Boxer: The boxer instance.

        Raises:
            ValueError: If the boxer with the given ID does not exist.

        """
        city = cls.query.get(city_id)
        if city is None:
            logger.info(f"CIty with ID {city_id} not found.")
            raise ValueError(f"City with ID {city_id} not found.")
        return city
    
    @classmethod
    def getWeather(self) -> str:
        """Delete a boxer by ID.

        Args:
            boxer_id: The ID of the boxer to delete.

        Raises:
            ValueError: If the boxer with the given ID does not exist.

        """
        """
        boxer = cls.get_boxer_by_id(boxer_id)
        if boxer is None:
            logger.info(f"Boxer with ID {boxer_id} not found.")
            raise ValueError(f"Boxer with ID {boxer_id} not found.")
        db.session.delete(boxer)
        db.session.commit()
        logger.info(f"Boxer with ID {boxer_id} permanently deleted.")
        """


        try:
            key = os.getenv("WEATHER_KEY")

            url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={key}"

            response = requests.get(url)

            if response.status_code == 200:
                logger.info("Weather retrieved")
                data = response.json()
                return data.weather.description
            else:
                logger.info("No weather for that city.")
        except Exception as e:
            raise(f"Error with {e}")