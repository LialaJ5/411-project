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

    def clear_ring(self):
        """Clears the list of boxers.

        """
        if not self.ring:
            logger.warning("Attempted to clear an empty ring.")
            return
        logger.info("Clearing the boxers from the ring.")
        self.ring.clear()


 #CHANGE
    #formerly enter_ring
    def add_to_favorite(self, city_id: int):
        """Prepares a boxer by adding them to the ring for an upcoming fight.

        Args:
            boxer_id (int): The ID of the boxer to enter the ring.

        Raises:
            ValueError: If the ring already has two boxers (fight is full).
            ValueError: If the boxer ID is invalid or the boxer does not exist.

        """
        """
        if len(self.ring) >= 2:
            logger.error(f"Attempted to add boxer ID {boxer_id} but the ring is full")
            raise ValueError("Ring is full, cannot add more boxers.")

        try:
            boxer = Boxers.get_boxer_by_id(boxer_id)
        except ValueError as e:
            logger.error(str(e))
            raise

        logger.info(f"Adding boxer '{boxer.name}' (ID {boxer_id}) to the ring")

        self.ring.append(boxer_id)

        logger.info(f"Current boxers in the ring: {[Boxers.get_boxer_by_id(b).name for b in self.ring]}")


        """
        try:
            city = Cities.get_city_by_id(city_id)
        except:
            logger.error(str(e))
            raise
        
        logger.info(f"Adding city '{city.name}' (ID {city_id}) to the favorites")

        self.favorites.append(city_id)

        logger.info(f"Current cities in the favorites: {[Cities.get_city_by_id(b).name for b in self.favorites]}")

    def get_weather_city(self, city_id) -> None:

    #formerly get_boxers
    def get_all_cities_and_weather(self) -> List[Boxers]:
        """Retrieves the current list of boxers in the ring.

        Returns:
            List[Boxers]: A list of Boxers dataclass instances representing the boxers in the ring.

        """
        if not self.ring:
            logger.warning("Retrieving boxers from an empty ring.")
        else:
            logger.info(f"Retrieving {len(self.ring)} boxers from the ring.")

        now = time.time()
        boxers: List[Boxers] = []

        for boxer_id in self.ring:
            expired = boxer_id not in self._ttl or now > self._ttl[boxer_id]
            if expired:
                logger.info(f"TTL expired or missing for boxer {boxer_id}. Refreshing from DB.")
                boxer = Boxers.get_boxer_by_id(boxer_id)
                self._boxer_cache[boxer_id] = boxer
                self._ttl[boxer_id] = now + self.ttl_seconds
            else:
                logger.debug(f"Using cached boxer {boxer_id} (TTL valid).")
            boxers.append(self._boxer_cache[boxer_id])

        logger.info(f"Retrieved {len(boxers)} boxers from the ring.")
        return boxers

    def get_fighting_skill(self, boxer: Boxers) -> float:
        """Calculates the fighting skill for a boxer based on arbitrary rules.

        The fighting skill is computed as:
        - Multiply the boxer's weight by the number of letters in their name.
        - Subtract an age modifier (if age < 25, subtract 1; if age > 35, subtract 2).
        - Add a reach bonus (reach / 10).

        Args:
            boxer (Boxers): A Boxers dataclass representing the combatant.

        Returns:
            float: The calculated fighting skill.

        """
        logger.info(f"Calculating fighting skill for {boxer.name}: weight={boxer.weight}, age={boxer.age}, reach={boxer.reach}")

        # Arbitrary calculations
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier

        logger.info(f"Fighting skill for {boxer.name}: {skill:.3f}")
        return skill

    #formerly clear_cache
    def clear_cities(self):
        """Clears the local TTL cache of boxer objects.

        """
        logger.info("Clearing local boxer cache in RingModel.")
        self._boxer_cache.clear()
        self._ttl.clear()

    def get_forecast_city(self, city_id) -> None:

        