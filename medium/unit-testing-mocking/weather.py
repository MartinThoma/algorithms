# Core Library modules
import hashlib
import hmac
import os
from base64 import b64encode
from typing import Dict

# Third party modules
import requests


def get_forecast(lat, lon, api_key):
    """Get the weather of tomorrow in a natural language sentence."""
    base_url = f"http://api.openweathermap.org/data/2.5/forecast"
    url = f"{base_url}?lat={lat}&lon={lon}&APPID={api_key}&units=metric"
    response = requests.get(url)
    tomorrow: Dict[str, Any] = response.json()["list"][1]
    temp = tomorrow["main"]["temp"]
    if temp < 0.0:
        tmp_str = "It's freezing "
    elif temp < 10.0:
        tmp_str = "It's cold "
    elif temp < 20:
        tmp_str = "It's comfortable "
    elif temp < 25:
        tmp_str = "It's warm, "
    clouds = tomorrow["clouds"]["all"]
    if clouds < 10:
        tmp_str += "and the sky is clear."
    elif clouds > 60:
        tmp_str += "and cloudy."
    return tmp_str.strip() + "."


if __name__ == "__main__":
    api_key = os.environ["OPEN_API_KEY"]
    print(get_forecast(48.1348643, 11.5790249, api_key))
