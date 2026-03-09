import pytest
from ai_virtual_development_team.generated_app import build_receive_business_requirements, build_generate_user_stories, \
    build_generate_implementation_code, build_auto_create_tests, build_report_progress_to_pm

def test_generated_app_integration():
    business_requirements = {"business_requirements": "New feature: User registration"}
    user_stories = build_receive_business_requirements(business_requirements)
    implementation_code = build_generate_user_stories(user_stories)
    tests = build_generate_implementation_code(implementation_code)
    progress = build_auto_create_tests(tests)
    final_output = build_report_progress_to_pm(progress)

    assert final_output is not None
    assert isinstance(final_output, dict)
    assert "story_id" in final_output
    assert "status" in final_output

    # You can add more assertions here to validate the values of 'story_id' and 'status'
