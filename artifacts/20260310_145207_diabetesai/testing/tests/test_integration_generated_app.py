"""Integration tests for generated modules."""

from generated_app.diabetes_prediction_system_patient_data_collection import build_diabetes_prediction_system_patient_data_collection
from generated_app.diabetes_prediction_system_predict_diabetes_risk import build_diabetes_prediction_system_predict_diabetes_risk
from generated_app.diabetes_prediction_system_integration_with_ehr import build_diabetes_prediction_system_integration_with_ehr


def test_generated_app_integration():
    result_1 = build_diabetes_prediction_system_patient_data_collection({'input': 'sample'})
    assert isinstance(result_1, dict)
    result_2 = build_diabetes_prediction_system_predict_diabetes_risk({'input': 'sample'})
    assert isinstance(result_2, dict)
    result_3 = build_diabetes_prediction_system_integration_with_ehr({'input': 'sample'})
    assert isinstance(result_3, dict)
