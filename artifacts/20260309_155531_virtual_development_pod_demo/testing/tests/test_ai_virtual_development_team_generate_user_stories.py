import pytest
from generated_app.ai_virtual_development_team_generate_user_stories import build_ai_virtual_development_team_generate_user_stories

def test_import():
    """Test importing the generate_user_stories module."""
    from generated_app.ai_virtual_development_team_generate_user_stories import build_ai_virtual_development_team_generate_user_stories

    assert build_ai_virtual_development_team_generate_user_stories is not None

def test_generate_user_stories_output_contract():
    """Test the output contract of generate_user_stories function."""
    business_requirement = "Business requirement 1"
    expected_user_story = {
        "id": "US-001",
        "title": "",
        "persona": "",
        "goals": [],
        "benefits": [],
        "acceptance_criteria": [],
    }

    user_stories = build_ai_virtual_development_team_generate_user_stories(business_requirement)

    assert isinstance(user_stories, list)
    assert all(isinstance(user_story, dict) for user_story in user_stories)
    assert all(isinstance(user_story, expected_user_story) for user_story in user_stories)

def test_generate_user_stories_acceptance_criteria():
    """Test that user stories have acceptance criteria."""
    business_requirement = "Business requirement 1: The system should display user profiles."
    expected_user_story = {
        "id": "US-001",
        "title": "Display user profiles",
        "persona": "User",
        "goals": ["View user information"],
        "benefits": ["Understand user details"],
        "acceptance_criteria": ["User can view their profile", "User can view other users' profiles"],
    }

    user_stories = build_ai_virtual_development_team_generate_user_stories(business_requirement)

    assert len(user_stories) == 1
    assert user_stories[0] == expected_user_story
