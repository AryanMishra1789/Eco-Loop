import requests


class WeatherTool:
    """
    Weather Tool

    Retrieves current weather information for a city.
    """

    BASE_URL = "https://wttr.in"

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def get_current_weather(self, city):
        """
        Get current weather for a city.
        """

        try:

            url = f"{self.BASE_URL}/{city}?format=j1"

            response = requests.get(url, timeout=10)

            response.raise_for_status()

            data = response.json()

            current = data["current_condition"][0]

            return {

                "city": city,

                "temperature": float(current["temp_C"]),

                "humidity": int(current["humidity"]),

                "wind_speed": float(current["windspeedKmph"]),

                "weather": current["weatherDesc"][0]["value"],

                "success": True

            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)

            }

    # ---------------------------------------------------------

    def get_forecast(self, city):
        """
        Return a simple three-day forecast.
        """

        try:

            url = f"{self.BASE_URL}/{city}?format=j1"

            response = requests.get(url, timeout=10)

            response.raise_for_status()

            data = response.json()

            forecast = []

            for day in data["weather"]:

                forecast.append({

                    "date": day["date"],

                    "max_temp": float(day["maxtempC"]),

                    "min_temp": float(day["mintempC"]),

                    "sun_hours": day["sunHour"]

                })

            return {

                "city": city,

                "forecast": forecast,

                "success": True

            }

        except Exception as e:

            return {

                "success": False,

                "error": str(e)

            }