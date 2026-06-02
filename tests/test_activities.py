"""
Tests for the activities endpoint (GET /activities).
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    
    # Verify all expected activities are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Music Ensemble",
        "Science Club",
        "Debate Team"
    ]
    
    for activity in expected_activities:
        assert activity in activities


def test_activity_has_required_fields(client):
    """Test that each activity has the required structure"""
    response = client.get("/activities")
    activities = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"


def test_activity_participants_is_list(client):
    """Test that participants field is a list for all activities"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list), \
            f"Participants for '{activity_name}' is not a list"


def test_activity_max_participants_is_positive(client):
    """Test that max_participants is a positive integer"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["max_participants"], int)
        assert activity_data["max_participants"] > 0, \
            f"Activity '{activity_name}' has non-positive max_participants"


def test_participants_count_does_not_exceed_max(client):
    """Test that number of participants doesn't exceed max_participants"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        participants_count = len(activity_data["participants"])
        max_participants = activity_data["max_participants"]
        assert participants_count <= max_participants, \
            f"Activity '{activity_name}' has more participants than max"
