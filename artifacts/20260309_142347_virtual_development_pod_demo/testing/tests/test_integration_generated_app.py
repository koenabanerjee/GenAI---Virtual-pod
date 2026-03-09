"""Integration tests for generated modules."""

from generated_app.build_an_ai_based_disease_prediction_system import build_build_an_ai_based_disease_prediction_system


def test_generated_app_integration():
    result_1 = build_build_an_ai_based_disease_prediction_system({'input': 'sample'})
    assert isinstance(result_1, dict)
