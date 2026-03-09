"""Integration tests for generated modules."""

from generated_app.build_an_app_with_login_and_reporting import build_build_an_app_with_login_and_reporting


def test_generated_app_integration():
    result_1 = build_build_an_app_with_login_and_reporting({'input': 'sample'})
    assert isinstance(result_1, dict)
