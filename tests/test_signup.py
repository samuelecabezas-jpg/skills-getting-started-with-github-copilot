"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup).
"""

import pytest


def test_signup_successful(client):
    """Test successful signup for an activity"""
    # Get initial participant count
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before["Chess Club"]["participants"])
    
    # Attempt signup
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    assert "message" in response.json()
    assert "newstudent@mergington.edu" in response.json()["message"]
    
    # Verify participant was added
    activities_after = client.get("/activities").json()
    new_count = len(activities_after["Chess Club"]["participants"])
    assert new_count == initial_count + 1
    assert "newstudent@mergington.edu" in activities_after["Chess Club"]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signup for non-existent activity returns 404"""
    response = client.post(
        "/activities/NonExistentActivity/signup?email=test@mergington.edu"
    )
    
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_email_returns_400(client):
    """Test that duplicate signup returns 400"""
    # First signup
    response1 = client.post(
        "/activities/Chess%20Club/signup?email=duplicate@mergington.edu"
    )
    assert response1.status_code == 200
    
    # Attempt duplicate signup
    response2 = client.post(
        "/activities/Chess%20Club/signup?email=duplicate@mergington.edu"
    )
    
    assert response2.status_code == 400
    assert "detail" in response2.json()
    assert "already signed up" in response2.json()["detail"]


def test_signup_already_existing_participant_returns_400(client):
    """Test that signup with already existing participant returns 400"""
    # Try to sign up someone already registered
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )
    
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "already signed up" in response.json()["detail"]


def test_signup_multiple_activities(client):
    """Test that same student can signup for multiple activities"""
    email = "multi@mergington.edu"
    
    # Sign up for first activity
    response1 = client.post(
        f"/activities/Chess%20Club/signup?email={email}"
    )
    assert response1.status_code == 200
    
    # Sign up for second activity
    response2 = client.post(
        f"/activities/Programming%20Class/signup?email={email}"
    )
    assert response2.status_code == 200
    
    # Verify both signups succeeded
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Programming Class"]["participants"]
