import pytest
from generated_app.ai_virtual_development_team import AIVirtualDevelopmentTeam

@pytest.fixture
def ai_virtual_development_team():
    return AIVirtualDevelopmentTeam()

def test_import(ai_virtual_development_team):
    """Test that the AIVirtualDevelopmentTeam module can be imported."""
    assert ai_virtual_development_team is not None

def test_build_report_output_contract(ai_virtual_development_team):
    """Test that the build_ai_virtual_development_team_report_progress_to_pm function returns a valid report."""
    report = ai_virtual_development_team.build_ai_virtual_development_team_report_progress_to_pm()
    assert isinstance(report, dict)
    assert set(report.keys()).issubset({"completed_user_stories", "remaining_user_stories", "unresolved_risks"})

def test_report_progress_acceptance_criteria(ai_virtual_development_team):
    """Test that the AI Virtual Development Team reports progress to the Project Manager with the correct information."""
    completed_user_stories = 3
    remaining_user_stories = 5
    unresolved_risks = 2

    ai_virtual_development_team.completed_user_stories = completed_user_stories
    ai_virtual_development_team.remaining_user_stories = remaining_user_stories
    ai_virtual_development_team.unresolved_risks = unresolved_risks

    report = ai_virtual_development_team.build_ai_virtual_development_team_report_progress_to_pm()

    assert report["completed_user_stories"] == completed_user_stories
    assert report["remaining_user_stories"] == remaining_user_stories
    assert report["unresolved_risks"] == unresolved_risks
