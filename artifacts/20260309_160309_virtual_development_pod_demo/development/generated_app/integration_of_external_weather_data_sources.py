"""Auto-generated module for US-002: Integration of external weather data sources."""

from __future__ import annotations
import requests
import json
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class IntegrationOfExternalWeatherDataSourcesService:
    """Implementation class aligned to user story US-002."""

    story_id: str = "US-002"

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        external_data_sources = payload.get("external_data_sources", [])
        fetched_data = {}

        for source in external_data_sources:
            url = source["url"]
            api_key = source.get("api_key")
            response = requests.get(url, params={"api_key": api_key})
            data = response.json() if response.status_code == 200 else {}

            if not data:
                print(f"Error fetching data from {url}")
                continue

            source_id = source["id"]
            fetched_data[source_id] = data

        cleaned_data = {}
        for source_id, data in fetched_data.items():
            try:
                cleaned_data[source_id] = {k: v for k, v in data.items() if v is not None}
            except Exception as e:
                print(f"Error cleaning data from {source_id}: {e}")

        database = payload.get("database")
        if database:
            database.store(cleaned_data)

        result = {
            "story_id": self.story_id,
            "status": "implemented",
            "input": payload,
            "summary": "Integrated external weather data sources",
            "acceptance": {
                "fetched_data": fetched_data,
                "cleaned_data": cleaned_data,
            },
        }
        return result


def build_integration_of_external_weather_data_sources(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Function entrypoint used by generated tests and integration flows."""
    return IntegrationOfExternalWeatherDataSourcesService().execute(payload)
