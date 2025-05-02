from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# from flask_cors import CORS

from config import ProductionConfig

from weatherFolder.db import db
from weatherFolder.models.cities_model import Cities
from weatherFolder.models.favorites_model import FavoritesModel
from weatherFolder.models.user_model import Users
from weatherFolder.utils.logger import configure_logger


load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    configure_logger(app.logger)

    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.filter_by(username=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return make_response(jsonify({
            "status": "error",
            "message": "Authentication required"
        }), 401)


    favorites_model = FavoritesModel()


    ####################################################
    #
    # Healthchecks
    #
    ####################################################


    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """
        Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.

        """
        app.logger.info("Health check endpoint hit")
        return make_response(jsonify({
            'status': 'success',
            'message': 'Service is running'
        }), 200)


    ##########################################################
    #
    # User Management
    #
    #########################################################

    @app.route('/api/create-user', methods=['PUT'])
    def create_user() -> Response:
        """Register a new user account.

        Expected JSON Input:
            - username (str): The desired username.
            - password (str): The desired password.

        Returns:
            JSON response indicating the success of the user creation.

        Raises:
            400 error if the username or password is missing.
            500 error if there is an issue creating the user in the database.
        """
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            Users.create_user(username, password)
            return make_response(jsonify({
                "status": "success",
                "message": f"User '{username}' created successfully"
            }), 201)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"User creation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while creating user",
                "details": str(e)
            }), 500)

    @app.route('/api/login', methods=['POST'])
    def login() -> Response:
        """Authenticate a user and log them in.

        Expected JSON Input:
            - username (str): The username of the user.
            - password (str): The password of the user.

        Returns:
            JSON response indicating the success of the login attempt.

        Raises:
            401 error if the username or password is incorrect.
        """
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            if Users.check_password(username, password):
                user = Users.query.filter_by(username=username).first()
                login_user(user)
                return make_response(jsonify({
                    "status": "success",
                    "message": f"User '{username}' logged in successfully"
                }), 200)
            else:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid username or password"
                }), 401)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 401)
        except Exception as e:
            app.logger.error(f"Login failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred during login",
                "details": str(e)
            }), 500)

    @app.route('/api/logout', methods=['POST'])
    @login_required
    def logout() -> Response:
        """Log out the current user.

        Returns:
            JSON response indicating the success of the logout operation.

        """
        logout_user()
        return make_response(jsonify({
            "status": "success",
            "message": "User logged out successfully"
        }), 200)

    @app.route('/api/change-password', methods=['POST'])
    @login_required
    def change_password() -> Response:
        """Change the password for the current user.

        Expected JSON Input:
            - new_password (str): The new password to set.

        Returns:
            JSON response indicating the success of the password change.

        Raises:
            400 error if the new password is not provided.
            500 error if there is an issue updating the password in the database.
        """
        try:
            data = request.get_json()
            new_password = data.get("new_password")

            if not new_password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "New password is required"
                }), 400)

            username = current_user.username
            Users.update_password(username, new_password)
            return make_response(jsonify({
                "status": "success",
                "message": "Password changed successfully"
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Password change failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while changing password",
                "details": str(e)
            }), 500)

    @app.route('/api/reset-users', methods=['DELETE'])
    def reset_users() -> Response:
        """Recreate the users table to delete all users.

        Returns:
            JSON response indicating the success of recreating the Users table.

        Raises:
            500 error if there is an issue recreating the Users table.
        """
        try:
            app.logger.info("Received request to recreate Users table")
            with app.app_context():
                Users.__table__.drop(db.engine)
                Users.__table__.create(db.engine)
            app.logger.info("Users table recreated successfully")
            return make_response(jsonify({
                "status": "success",
                "message": f"Users table recreated successfully"
            }), 200)

        except Exception as e:
            app.logger.error(f"Users table recreation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while deleting users",
                "details": str(e)
            }), 500)

    ##########################################################
    #
    # Cities
    #
    ##########################################################    

    @app.route('/api/get-city-by-id/<int:city_id>', methods=['GET'])
    @login_required
    def get_city_by_id(city_id: int) -> Response:
        """Route to get a city by its id.

        Path Parameter:
            - city_id (int): The ID of the city.

        Returns:
            JSON response containing the city details if found.

        Raises:
            400 error if the city is not found.
            500 error if there is an issue retrieving the city from the database.

        """
        try:
            app.logger.info(f"Received request to retrieve city with ID {city_id}")

            city = Cities.get_city_by_id(city_id)

            if not city:
                app.logger.warning(f"City with ID {city_id} not found.")
                return make_response(jsonify({
                    "status": "error",
                    "message": f"City with ID {city_id} not found"
                }), 400)

            app.logger.info(f"Successfully retrieved city: {city}")
            return make_response(jsonify({
                "status": "success",
                "city": city
            }), 200)

        except Exception as e:
            app.logger.error(f"Error retrieving city with ID {city_id}: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while retrieving the city",
                "details": str(e)
            }), 500)

    ############################################################
    #
    # Favorites
    #
    ############################################################

    @app.route('/api/add-to-favorite/<int:city_id>', methods=['POST'])
    @login_required
    def add_to_favorite(city_id: int) -> Response:
        """Route to add a city to model favorites.

        Path Parameter:
            - city_id (int): The ID of the city.

        Returns:
            JSON response indicating success of the operation.

        Raises:
            400 error if the city is not found.
            500 error if there is an issue retrieving the city from the database.

        """
        try:
            app.logger.info("")
            data = request.json()
            city_name = data.get("name")

            if not city_name:
                app.logger.warning("Attempted to add a city wuthout specifying name.")
                return make_response(jsonify({
                    "status":  "error",
                    "message": "You must name a city."
                }), 400)

            app.logger.info(f"Attempting to add city {city_name} to favorites.")

            city = Cities.get_city_by_name(city_name)

            if not city:
                app.logger.warning(f"City '{city_name}' not found.")
                return make_response(jsonify({
                    "status": "error",
                    "message": f"City '{city_name}' not found.",
                }), 400)
        
            try:
                favorites_model.add_to_favorites(city.id)
            except ValueError as e:
                app.logger.warning(f"Cannot enter {city.name}: e")
                return make_response(jsonify({
                    "status": "error",
                    "message": str(e)
                }), 400)
        
            cities = [Cities.get_city_by_id(b) for b in favorites_model.favorites]

            app.logger.info(f"City '{city_name}' added to favorite. Current cities: {cities}")

            return make_response(jsonify({
                "status": "success",
                "message": f"City '{city_name} is now in your favorites.",
            }), 200)

        except Exception as e:
            app.logger.error(f"Failed to add city to your favorites: {e}")
            return make_response (jsonify ({
                "status": "error",
                "message": "An internal error occured while entering city in favorite.",
                "cities": cities
            }), 200)

    @app.route('/api/get-weather-city/<int:city_id>', methods=['GET'])
    @login_required
    def get_weather_city(city_id: int) -> Response:
        """Route to get the weather of city by its ID.

        Path Parameter:
            - city_id (int): The ID of the city.

        Returns:
            JSON response containing the weather details if found.

        Raises:
            400 error if the city is not found.
            500 error if there is an issue retrieving the city from the database.

        """
        try:
            app.logger.info("Retrieving weather of city...")

            data = request.json()
            city_id = data.get("id")

            if not city_id:
                app.logger.warning("Attempted to retrieve weather without giving city.")
                return make_response(jsonify({
                    "status": "error",
                    "message": "You must give city id"
                }), 400)
            
            app.logger.info(f"Attempting to retrieve city '{city_id}' weather.")

            try:
                weather = Cities.get_weather_city(city_id)
            except ValueError as e:
                app.logger.warning(f"Cannot retrieve {city_id}: {e}")
                return make_response(jsonify({
                    "status": "error",
                    "message": str(e)
                }), 400)
            
            app.logger.info(f"Retrieved weather of city {city_id}.")
            
            return make_response(jsonify({
                "status": "success",
                "message": f"City '{city_id}' weather is.",
                "weather": weather
            }), 200)
        
        except Exception as e:
            app.logger.error(f"Failed to retrieve weather of the city: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred retrieving weather of city",
                "details": str(e)
            }), 500)
    
    @app.route('/api/clear-favorites', methods=['DELETE'])
    @login_required
    def clear_favorites() -> Response:
        """Route to clear the list of cities from model favorites.

        Returns:
            JSON response indicating success of the operation.

        Raises:
            500 error if there is an issue clearing cities.

        """
        try:
            app.logger.info("Clearing favorite cities...")

            favorites_model.clear_favorites()

            app.logger.info("Cities cleared from favorites successfully.")
            return make_response(jsonify({
                "status": "success",
                "message": "Cities have been cleared from favorites."
            }), 200)

        except Exception as e:
            app.logger.error(f"Failed to clear city: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while clearing cities",
                "details": str(e)
            }), 500)

    @app.route('/api/get-forecast-city/<int:city_id>', methods=['POST'])
    @login_required
    def get_forecast_city(city_id: int) -> Response:
        """Route to get the forecast of a city.

        Path Parameter:
            - city_id (int): The ID of the city.

        Returns:
            JSON response containing the city forecast details if found.

        Raises:
            400 error if the city is not found.
            500 error if there is an issue retrieving the city from the database.

        """
        try:
            app.logger.info("Retrieving forecast of city...")

            data = request.json()
            city_id = data.get("id")

            if not city_id:
                app.logger.warning("Attempting to retrieve forecast without the city")
                return make_response(jsonify({
                    "status": "error",
                    "message": "You must give an id."
                }), 400)
            
            app.logger.info(f"Attempting to retrieve forecast of city {city_id}.")

            try:
                forecast = Cities.get_forecast_city(city_id)
            except ValueError as e:
                app.logger.warning(f"Could not get city with id {city_id}.")
                return make_response(jsonify({
                    "status": "error",
                    "message": str(e)
                }), 400)
            
            app.logger.info("Retrieved forecast of city.")

            return make_response(jsonify({
                "status": "success",
                "forecast": forecast
            }), 200)
        
        except Exception as e:
            app.logger.error(f"Failed to retrieve the foreacast: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while retrieving forecast.",
                "details": str(e)
            }), 500)
    
    @app.route('/api/get-all_cities_and_weather', methods=['GET'])
    @login_required
    def get_all_cities_and_weather() -> Response:
        """Route to get the list of cities and their weathers.

        Returns:
            JSON response with the list of cities and weathers.

        Raises:
            500 error if there is an issue getting the cities.

        """
        try:
            app.logger.info("Retrieving all cities with weathers")

            cities_weathers = favorites_model.get_all_cities_and_weather()

            app.logger.info("Retrieved all cities and with their corresponding weather.")
            
            return make_response(jsonify({
                "status": "successs",
                "cities_weathers": cities_weathers
            }), 200)

        except Exception as e:
            app.logger.error(f"Failed to retrieve cities with weather: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while retrieving cities.",
                "details": str(e)
            }), 500)

    return app

if __name__ == '__main__':
    app = create_app()
    app.logger.info("Starting Flask app...")
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        app.logger.error(f"Flask app encountered an error: {e}")
    finally:
        app.logger.info("Flask app has stopped.")