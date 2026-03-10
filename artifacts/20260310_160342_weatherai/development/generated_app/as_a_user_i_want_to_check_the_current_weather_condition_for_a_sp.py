"""Auto-generated module for US-001: As a user, I want to check the current weather condition for a specific location."""

from __future__ import annotations
import requests
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AsAUserIWantToCheckTheCurrentWeatherConditionForASpecificLocationService:
    """Implementation class aligned to user story US-001."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        location = payload["location"]
        response = self._get_weather_data(location)
        result = {
            "story_id": self.story_id,
            "status": "implemented",
            "input": payload,
            "summary": "Checks the current weather condition for a specific location and returns temperature, weather condition, and humidity.",
            "acceptance": {
                "The user can enter a location (city or zip code)": location in payload,
                "The app displays the current temperature, weather condition, and humidity for the entered location": "output" in response and "temperature" in response and "weather" in response and "humidity" in response,
                "The app updates the weather information in real-time": False, # Real-time updates are not possible with this implementation
            },
            "output": response,
        }
        return result

    def _get_weather_data(self, location: str) -> Dict[str, Any]:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}"
        response = requests.get(url).json()
        output = {
            "temperature": response["main"]["temp"],
            "weather": response["weather"][0]["description"],
            "humidity": response["main"]["humidity"],
        }
        return output


def build_as_a_user_i_want_to_check_the_current_weather_condition_for_a_sp(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    weather_service = AsAUserIWantToCheckTheCurrentWeatherConditionForASpecificLocationService("your_api_key_here")
    return weather_service.execute(payload)
