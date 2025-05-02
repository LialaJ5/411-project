**Weather App**  
James Le, Liala Jama, Yingtong Shen

**Overview:**  
Our project is a simple weather app that allows users to keep track of the current weather and forecast of their favorite cities. Our app has five main functionalities:

1. The option to add a city to a list to track it  
   1. Allows users to add a city to their list of favorite locations by specifying its unique ID. This feature ensures quick access to preferred cities for weather tracking without needing to search repeatedly. The system logs the addition and confirms the updated favorites list.  
2. Getting the current weather of a city on the favorites list  
   1. Retrieves the current weather conditions for a specified city that has been marked as a favorite. This feature provides immediate access to up-to-date weather data such as general conditions and temperatures, helping users stay informed about locations they care about.  
3. Get weather for all favorite cities on the list at once  
   1. Displays a list of all cities saved to the user's favorites along with the current weather for each. This consolidated view allows users to monitor multiple locations at once, making it easy to compare weather conditions across their selected areas of interest.  
4. Clearing the favorites list  
   1. Allows users to remove all cities from their list of saved favorites.This feature is useful for quickly resetting or managing saved locations without needing to remove them one by one.If the list is already empty, the system will log a warning and take no further action, preventing unnecessary operations.  
5. Getting the forecast for a favorite city  
   1. Offers a multi-day weather forecast for a specific city that has been saved to the user's favorites.The forecast includes expected high and low temperatures, precipitation chances, and descriptive weather conditions for each of the coming days.This feature enables users to make informed plans based on predicted atmospheric changes in their preferred locations

**Api:** [Weather API](https://openweathermap.org/api)

**Routes**  
**Route 1:** /create\_user

* **Request Type:** PUT  
* **Purpose:** creates a new user with associated password  
* **Request Body:**  
  * Username (String): the desired username  
  * Password (String): the desired password  
* **Response Format:** JSON  
  * Code: 201  
  * Content: "User '{username}' created successfully"  
* **Example Request:**  
  **{**  
  	“Username”: “a123”,  
  	“Password: “securepassword”  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“User a123 created successfully”  
  **}**

**Route 2:** /login

* **Request Type:** POST  
* **Purpose:** Authenticate a user and log them in  
* **Request Body:**  
  * Username (String): the username of the user  
  * Password (String): the password of the user  
* **Response Format:** JSON  
  * Code: 200  
  * Content: "User '{username}' logged in successfully"  
* **Example Request:**  
  **{**  
  	“Username”: “a123”,  
  	“Password: “securepassword”  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“User a123 logged in successfully”  
  **}**

**Route 3:** /logout

* **Request Type:** PUT  
* **Purpose:**  Logs out a user  
* **Request Body:**  
  * N/A  
* **Response Format:** JSON  
  * Code: 200  
  * Content: "User logged out successfully"  
* **Example Request:**  
  **{**  
  	logout\_user()  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“User logged out successfully”  
  **}**


**Route 4:** /change\_password

* **Request Type:** POST  
* **Purpose:** change password of current user  
* **Request Body:**  
  * New Password (String): the new password to be set  
* **Response Format:** JSON  
  * Code: 200  
  * Content: "Password changed successfully"  
* **Example Request:**  
  **{**  
  	“NewPassword: 1234”  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“Password changed successfully”  
  **}**

**Route 5:** /reset\_user

* **Request Type:** Delete  
* **Purpose:** deletes all users  
* **Request Body:**  
  * Request to delete all users  
* **Response Format:** JSON  
  * Code: 201  
  * Content: “Users table recreated successfully”  
* **Example Request:**  
  **{**  
  	“Received request to recreate Users table”  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“Users table recreated successfully”  
  **}**  
  


**Route 6:** /get-city-by-id

* **Request Type:** Get  
* **Purpose:** gets the name of the city by id  
* **Request Body:**  
  * City\_id (int): The ID of the city  
* **Response Format:** JSON  
  * Code: 200  
  * Content: “Successfully retrieved city: {city}”  
* **Example Request:**  
  **{**  
  	**“**Received request to retrieve city with ID 2”  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“City: Boston”  
  **}**

**Route 7:** /add-to-favorite

* **Request Type:** Post  
* **Purpose:** Add a city to our list of favorites  
* **Request Body:**  
  * City\_name (int): The name of the city  
* **Response Format:** JSON  
  * Code: 200  
  * Content: “City {city\_name} is now in your favorites”  
* **Example Request:**  
  **{**  
  	**“**Attempting to add Boston to favorites”  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“City Boston is now in your favorites”  
  **}**


**Route 8:** /get-weather-city

* **Request Type:** Get  
* **Purpose:** Get weather of city by ID  
* **Request Body:**  
  * City\_id (int): The ID of the city  
* **Response Format:** JSON  
  * Code: 200  
  * Content: “Retrieved weather of city {city\_id}”  
* **Example Request:**  
  **{**  
  	**“**Retrieving weather of city…”  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“Message: City Boston weather is…”  
  	“Weather: sunny”  
  **}**


  
**Route 8:** /clear-favorites

* **Request Type:** Post  
* **Purpose:** clearing the list of favorite cities  
* **Request Body:**  
  * Clearing favorite cities…  
* **Response Format:** JSON  
  * Code: 200  
  * Content: “ cities have been cleared from favorites”  
* **Example Request:**  
  **{**  
  	**“**Clearing favorite cities…”  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“Message: cities have been cleared from favorites”  
  **}**


**Route 9:** /get-forecast-city

* **Request Type:** Post  
* **Purpose:** get weather forecast for a city  
* **Request Body:**  
  * City\_id (int): The ID of the city  
* **Response Format:** JSON  
  * Code: 200  
  * Content: “forecast: {forecast}”  
* **Example Request:**  
  **{**  
  	**“**Attempting to retrieve forecast of city Boston”  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“Forecast: sunny tomorrow”  
  **}**




**Route 10:** /get-all-cities-and-weather

* **Request Type:** Get  
* **Purpose:** get all cities and weather from lists  
* **Request Body:**  
  * Retrieving all cities with weathers  
* **Response Format:** JSON  
  * Code: 200  
  * Content: “cities\_weathers: {cities\_weathers}”  
* **Example Request:**  
  **{**  
  	**“**Retrieving all cities with weathers”  
  **}**  
* **Example Response:**  
  **{**  
  	“Status: success”,  
  	“Cities\_weathers: \[(Boston, sunny), (New York, rainy), (Los Angeles, cloudy)\]”  
  **}**

