"""Auto-generated module for US-002: As a user, I want to view the weather forecast for the next 5 days."""

from __future__ import annotations
import requests
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class AsAUserIWantToViewTheWeatherForecastForTheNext5DaysService:
    """Implementation class aligned to user story US-002."""

    def __init__(self, api_key: str, location_service: Any):
        self.api_key = api_key
        self.location_service = location_service

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        location = self.location_service.get_location()
        response = requests.get(
            f"http://openweathermap.org/data/2.5/forecast?q={location['name']}&appid={self.api_key}"
        )
        response.raise_for_status()
        weather_data = response.json()

        result: Dict[str, Any] = {
            "story_id": self.story_id,
            "status": "implemented",
            "input": payload,
            "summary": "Display a 5-day weather forecast for the user's current location",
            "acceptance": {
                "The user can view a 5-day weather forecast for their current location": [
                    lambda: len(weather_data["list"]) == 5,
                    "Error: Incorrect number of days in the forecast",
                ],
                "Each day in the forecast includes the temperature, weather condition, and precipitation probability": [
                    lambda: all(
                        all(
                            all(
                                [
                                    "temp" in day,
                                    "weather" in day,
                                    "pop" in day
                                ]
                            )
                            for day in weather_data["list"]
                        )
                    ),
                    "Error: Missing required data in the forecast",
                ],
                "The app updates the forecast information daily": [
                    lambda: False,
                    "Note: This acceptance criteria is not implemented in this service",
                ],
            },
        }

        result["forecast"] = [
            {
                "day": day["dt_txt"][:10],
                "temperature": day["main"]["temp"],
                "condition": day["weather"][0]["main"],
                "description": day["weather"][0]["description"],
                "icon": day["weather"][0]["icon"],
                "precipitation_probability": day["pop"],
            }
            for day in weather_data["list"]
        ]

        return result


def build_as_a_user_i_want_to_view_the_weather_forecast_for_the_next_5_days(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    weather_service = AsAUserIWantToViewTheWeatherForecastForTheNext5DaysService(
        api_key="your_api_key_here",
        location_service=payload["location_service"],
    )
    return weather_service.execute(payload)
