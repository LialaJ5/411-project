import logging
import math
import os
import time
import requests
from typing import List

from weatherFolder.models.cities_model import Cities
from weatherFolder.utils.logger import configure_logger
from weatherFolder.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class FavoritesModel:
    """A class to manage the list of favorite cities selected by the user.

    """

 
    def __init__(self):
        """Initializes the FavoritesModel with an empty list of favorite cities.
        
        Attributes:
            favorites (List[int]): A list of city IDs marked as favorites by the user.
        """

        self.favorites: List[int] = []


    def clear_favorites(self):
        """Clears the list of cities.
        """
        if not self.favorites:
            logger.warning("Attempted to clear an empty favorites.")
            return
        logger.info("Clearing the cities from the favorites.")
        self.favorites.clear()


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
        except RuntimeError as e:
            logger.error(str(e))
            raise
        
        logger.info(f"Adding city '{city.name}' (ID {city_id}) to the favorites")

        self.favorites.append(city_id)

        logger.info(f"Current cities in the favorites: {[Cities.get_city_by_id(b).name for b in self.favorites]}")

    def get_weather_city(self, city_id) -> str:
        """Get the current weather description for the specified favorite city.

        Args:
            city_id (int): The ID of the city for which to retrieve current weather.

        Returns:
            str: A short weather description (e.g., "clear sky", "light rain").

        Raises:
            ValueError: If the city does not exist.
            RuntimeError: If there is an error retrieving the weather from the external API.
        """
        logger.info(f"Getting weather for city with id {city_id}")
        try:
            city = Cities.get_city_by_id(city_id)
        except ValueError as e:
            logger.error(str(e))
            raise
        except RuntimeError as e:
            logger.error(str(e))
            raise
        
        weather = city.get_weather()
        return weather


    def get_all_cities_and_weather(self):
        """Retrieves the current list of cities in the list.

        Returns:
            List[Cities]: A list of Cities dataclass instances representing the cities in the favorites list.

        """
        if not self.favorites:
            logger.warning("Retrieving cities from an empty list.")
        else:
            logger.info(f"Retrieving {len(self.favorites)} cities from the list.")

        #now = time.time()
        cities = []

        for city_id in self.favorites:
            #expired = city_id not in self._ttl or now > self._ttl[city_id]
            #if expired:
            #    logger.info(f"TTL expired or missing for boxer {city_id}. Refreshing from DB.")
            city = Cities.get_city_by_id(city_id)
            weather = Cities.get_weather(city_id)
            #    self._boxer_cache[city_id] = city
            #   self._ttl[city_id] = now + self.ttl_seconds
            #else:
            #    logger.debug(f"Using cached boxer {city_id} (TTL valid).")
            cities.append((city,weather))

        logger.info(f"Retrieved {len(cities)} cities from favorites.")
        return cities
    

    def get_forecast_city(self, city_id: int) -> dict:
        """Get the weather forecast for the specified favorite city.

        Args:
            city_id (int): ID of the favorite city.

        Returns:
            dict: Contains the city name and a 5-day weather forecast.
            
        Raises:
            ValueError: If city_id is not in favorites or the city does not exist.
        """
        if city_id not in self.favorites:
            raise ValueError(f"City ID {city_id} is not in favorites.")
        
        try:
            city = Cities.get_city_by_id(city_id)
        except ValueError as e:
            logger.error(str(e))
            raise
        
        key = os.getenv("WEATHER_KEY")
        if not key:
            raise ValueError("Missing OpenWeatherMap API key.")
        
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={city.lat}&lon={city.lon}&appid={key}&units=metric"
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                logger.warning(f"Failed to fetch forecast for {city.name}: {response.status_code}")
                raise ValueError("Forecast API request failed.")
        
            data = response.json()
            forecast_list = data["list"]
        
            daily_forecast = []
            for entry in forecast_list:
                if "12:00:00" in entry["dt_txt"]:
                    daily_forecast.append({
                        "date": entry["dt_txt"].split(" ")[0],
                        "high": entry["main"]["temp_max"],
                        "low": entry["main"]["temp_min"],
                        "precipitation_chance": entry.get("pop", 0.0),
                        "condition": entry["weather"][0]["description"]
                    })
                
            logger.info(f"Retrieved {len(daily_forecast)} forecast entries for {city.name}")
        
            return {"city": city.name, "forecast": daily_forecast}
        
        except Exception as e:
            logger.error(f"Error fetching forecast for {city.name}: {e}")
            raise ValueError(f"Error fetching forecast: {e}")
