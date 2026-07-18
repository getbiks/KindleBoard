import requests
import time


LATITUDE = 19.2813
LONGITUDE = 72.8697


cache = {
    "time": 0,
    "data": None
}


def get_weather():

    # Cache for 10 minutes
    if cache["data"] and time.time() - cache["time"] < 600:
        return cache["data"]


    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={LATITUDE}"
        f"&longitude={LONGITUDE}"
        "&current="
        "temperature_2m,"
        "relative_humidity_2m,"
        "apparent_temperature,"
        "wind_speed_10m,"
        "weather_code"
    )


    try:

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()


        current = data["current"]


        weather = {
            "temperature": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "wind": current["wind_speed_10m"],
            "code": current["weather_code"]
        }


        cache["data"] = weather
        cache["time"] = time.time()


        return weather


    except Exception as e:

        return {
            "error": str(e)
        }



def weather_text():

    data = get_weather()

    if "error" in data:
        return "Weather unavailable"


    return (
        f"{data['temperature']} C\n"
        f"Feels {data['feels_like']} C\n"
        f"Humidity {data['humidity']}%\n"
        f"Wind {data['wind']} km/h"
    )
