import logging
import math
import os
import time
from typing import List

from weatherFolder.models.cities_model import Cities
from weatherFolder.utils.logger import configure_logger
from weatherFolder.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


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

#CHANGE (Finish)
    # Formerly clear_ring
    def clear_city(self):
        """Clears the list of cities.
        """
        if not self.favorites:
            logger.warning("Attempted to clear an empty favorites.")
            return
        logger.info("Clearing the cities from the favorites.")
        self.favorites.clear()

 #CHANGE (Finish)
    #formerly enter_ring
    def add_to_favorite(self, city_id: int):
        """Adds the specified city (by city ID) to the favorites list.

        Args:
            city_id (int): The ID of the city to enter the favorites.

        Raises:
            ValueError: If the City ID is invalid or the city does not exist.

        """
        try:
            city = Cities.get_city_by_id(city_id)
        except ValueError as e:
            logger.error(str(e))
            raise
        
        logger.info(f"Adding city '{city.name}' (ID {city_id}) to the favorites")

        self.favorites.append(city_id)

        logger.info(f"Current cities in the favorites: {[Cities.get_city_by_id(b).name for b in self.favorites]}")

    def get_weather_city(self, city_id) -> str:
        
        logger.info(f"Getting weather for city with id {city_id}")
        try:
            city = Cities.get_city_by_id(city_id)
        except ValueError as e:
            logger.error(str(e))
            raise
        
        weather = city.get_weather()
        return weather

    """
    #formerly get_boxers
    def get_all_cities_and_weather(self) -> List[str,str]:
        "Retrieves the current list of cities in the list.

        Returns:
            List[Cities]: A list of Cities dataclass instances representing the cities in the favorites list.

        "
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

    """

    """

    def get_fighting_skill(self, boxer: Boxers) -> float:
        "Calculates the fighting skill for a boxer based on arbitrary rules.

        The fighting skill is computed as:
        - Multiply the boxer's weight by the number of letters in their name.
        - Subtract an age modifier (if age < 25, subtract 1; if age > 35, subtract 2).
        - Add a reach bonus (reach / 10).

        Args:
            boxer (Boxers): A Boxers dataclass representing the combatant.

        Returns:
            float: The calculated fighting skill.

        "
        logger.info(f"Calculating fighting skill for {boxer.name}: weight={boxer.weight}, age={boxer.age}, reach={boxer.reach}")

        # Arbitrary calculations
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier

        logger.info(f"Fighting skill for {boxer.name}: {skill:.3f}")
        return skill
    """

    def get_forecast_city(self, city_id) -> None:
        return False
