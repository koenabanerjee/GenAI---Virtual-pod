import pytest
import json
from unittest.mock import MagicMock, patch
from generated_app.integration_of_external_weather_data_sources import (
    build_integration_of_external_weather_data_sources,
)

@pytest.fixture
def mock_external_weather_data():
    return {
        "city": "New York",
        "country": "USA",
        "temperature": 25.5,
        "humidity": 50,
        "weather": ["clouds", "rain"],
    }

@pytest.fixture
def mock_database():
    class MockDatabase:
        def save_data(self, data):
            self.data = data

        data = None

    return MockDatabase()

def test_build_integration_of_external_weather_data_sources_output_contract():
    assert callable(build_integration_of_external_weather_data_sources)

@patch("generated_app.integration_of_external_weather_data_sources.requests.get")
def test_fetching_weather_data_from_external_source(mock_get, mock_database):
    mock_get.return_value.json.return_value = mock_external_weather_data
    build_integration_of_external_weather_data_sources(mock_database)

    assert mock_database.data is not None
    assert isinstance(mock_database.data, dict)

@patch("generated_app.integration_of_external_weather_data_sources.requests.get")
@patch("generated_app.integration_of_external_weather_data_sources.json.loads")
def test_handling_different_formats_and_apis(mock_loads, mock_get, mock_database):
    mock_get.return_value.status_code = 200
    mock_get.return_value.headers = {"Content-Type": "application/xml"}
    mock_loads.return_value = mock_external_weather_data

    build_integration_of_external_weather_data_sources(mock_database)

    assert mock_database.data is not None
    assert isinstance(mock_database.data, dict)

@patch("generated_app.integration_of_external_weather_data_sources.requests.get")
@patch("generated_app.integration_of_external_weather_data_sources.json.loads")
def test_validating_and_cleaning_data(mock_loads, mock_get, mock_database):
    mock_get.return_value.json.return_value = {
        "city": "New York",
        "country": "USA",
        "temperature": "25.5°C",
        "humidity": 50,
        "weather": ["clouds", "rain"],
    }

    build_integration_of_external_weather_data_sources(mock_database)

    assert mock_database.data is not None
    assert isinstance(mock_database.data, dict)
    assert "temperature" in mock_database.data
    assert mock_database.data["temperature"] == 25.5
