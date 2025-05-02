import logging
from typing import List
import requests
import os
from dotenv import load_dotenv, dotenv_values

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from weatherFolder.db import db
from weatherFolder.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)

load_dotenv()

#CHANGE
class Cities(db.Model):
    """Represents a city with geographic coordinates.

    This SQLAlchemy model maps to the 'cities' table in the database and stores
    essential information such as the city's name, latitude, and longitude.
    Used for retrieving and displaying location-specific weather data.
    """
    
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    def __init__(self, name: str, lat: float, lon: float):
        """Initializes a new City instance with a name and geographic coordinates.

        Args:
            name (str): The name of the city.
            lat (float): The latitude of the city.
            lon (float): The longitude of the city.
        """
        self.name = name
        self.lat = lat
        self.lon = lon


 #CHANGE
    @classmethod
    def create_city(cls, name: str, lat: float, lon: float) -> None:
        """Creates and saves a new city record to the database.

        Args:
            name (str): The name of the city.
            lat (float): The latitude of the city.
            lon (float): The longitude of the city.

        Raises:
            ValueError: If a city with the same name already exists.
            SQLAlchemyError: If a database error occurs during creation.
        """
        logger.info(f"Creating boxer: {name}, {lat=} {lon=}")
        try:
            city = cls(name=name, lat=lat, lon=lon)
            db.session.add(city)
            db.session.commit()
            logger.info(f"City created!")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"City with name '{name}' already exists.")
            raise ValueError(f"City with name '{name}' already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during creation: {e}")
            raise

 #CHANGE
    @classmethod
    def get_city_by_id(cls, city_id: int) -> "Cities":
        """Retrieves a city from the database by its ID.

        Args:
            city_id (int): The ID of the city to retrieve.

        Returns:
            Cities: The corresponding city instance.

        Raises:
            ValueError: If no city with the specified ID exists.
        """
        city = db.session.get(cls, city_id)
        if city is None:
            logger.info(f"City with ID {city_id} not found.")
            raise ValueError(f"City with ID {city_id} not found.")
        return city


 #CHANGE
    def get_weather(self) -> str:
        """Fetches the current weather description for this city using its coordinates.

        Returns:
            str: A short textual description of the current weather (e.g., "clear sky").

        Raises:
            Exception: If the weather API request fails or an error occurs during retrieval.
        """
        try:
            key = os.getenv("WEATHER_KEY")

            url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={key}"

            response = requests.get(url)

            if response.status_code == 200:
                logger.info("Weather retrieved")
                data = response.json()
                return data["weather"][0]["description"]
            else:
                logger.info("No weather for that city.")
        except Exception as e:
            raise(f"Error with {e}")