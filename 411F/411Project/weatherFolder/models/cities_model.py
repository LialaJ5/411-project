import logging
from typing import List
import requests
import os
from dotenv import load_dotenv, dotenv_values

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from boxing.db import db
from boxing.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)

load_dotenv()

 #CHANGE
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


 #CHANGE
    @classmethod
    def create_city(cls, name: str, lat: float, lon: float) -> None:
        """Create and persist a new Boxer instance.

        Args:
            name: The name of the boxer.
            weight: The weight of the boxer.
            height: The height of the boxer.
            reach: The reach of the boxer.
            age: The age of the boxer.

        Raises:
            IntegrityError: If a boxer with the same name already exists.
            ValueError: If the weight is less than 125 or if any of the input parameters are invalid.
            SQLAlchemyError: If there is a database error during creation.

        """

        """
        logger.info(f"Creating boxer: {name}, {lat=} {lon=}")

        if weight < 125:
            raise ValueError("Weight must be at least 125.")
        if height <= 0:
            raise ValueError("Height must be greater than 0.")
        if reach <= 0:
            raise ValueError("Reach must be greater than 0.")
        if not (18 <= age <= 40):
            raise ValueError("Age must be between 18 and 40.")

        try:
            boxer = cls(name=name, weight=weight, height=height, reach=reach, age=age)
            db.session.add(boxer)
            db.session.commit()
            logger.info(f"Boxer created successfully: {name}")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Boxer with name '{name}' already exists.")
            raise ValueError(f"Boxer with name '{name}' already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during creation: {e}")
            raise
        
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


    @classmethod
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
    def get_boxer_by_name(cls, name: str) -> "Boxers":
        """Retrieve a boxer by name.

        Args:
            name: The name of the boxer.

        Returns:
            Boxer: The boxer instance.

        Raises:
            ValueError: If the boxer with the given name does not exist.

        """
        boxer = cls.query.filter_by(name=name).first()
        if boxer is None:
            logger.info(f"Boxer '{name}' not found.")
            raise ValueError(f"Boxer '{name}' not found.")
        return boxer

 #CHANGE
    @classmethod
    def getWeather(self) -> str:
        """Delete a boxer by ID.

        Args:
            boxer_id: The ID of the boxer to delete.

        Raises:
            ValueError: If the boxer with the given ID does not exist.

        """
        boxer = cls.get_boxer_by_id(boxer_id)
        if boxer is None:
            logger.info(f"Boxer with ID {boxer_id} not found.")
            raise ValueError(f"Boxer with ID {boxer_id} not found.")
        db.session.delete(boxer)
        db.session.commit()
        logger.info(f"Boxer with ID {boxer_id} permanently deleted.")

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

