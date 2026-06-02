"""
Tests for the unregister endpoint (DELETE /activities/{activity_name}/unregister).
"""

import pytest


def test_unregister_successful(client):
    """Test successful unregistration from an activity"""
    email = "unregister@mergington.edu"
    
    # First, sign up
    client.post(
        f"/activities/Chess%20Club/signup?email={email}"
    )
    
    # Verify signup was successful
    activities_before = client.get("/activities").json()
    assert email in activities_before["Chess Club"]["participants"]
    initial_count = len(activities_before["Chess Club"]["participants"])
    
    # Now unregister
    response = client.delete(
        f"/activities/Chess%20Club/unregister?email={email}"
    )
    
    assert response.status_code == 200
    assert "message" in response.json()
    assert email in response.json()["message"]
    
    # Verify participant was removed
    activities_after = client.get("/activities").json()
    new_count = len(activities_after["Chess Club"]["participants"])
    assert new_count == initial_count - 1
    assert email not in activities_after["Chess Club"]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregister from non-existent activity returns 404"""
    response = client.delete(
        "/activities/NonExistentActivity/unregister?email=test@mergington.edu"
    )
    
    assert response.status_code == 404
    assert "detail" in response.json()
    assert "Activity not found" in response.json()["detail"]


def test_unregister_email_not_registered_returns_400(client):
    """Test that unregister with non-registered email returns 400"""
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
    )
    
    assert response.status_code == 400
    assert "detail" in response.json()
    assert "not signed up" in response.json()["detail"]


def test_unregister_already_unregistered_returns_400(client):
    """Test that double unregister returns 400"""
    email = "double@mergington.edu"
    
    # Sign up
    client.post(
        f"/activities/Programming%20Class/signup?email={email}"
    )
    
    # Unregister first time
    response1 = client.delete(
        f"/activities/Programming%20Class/unregister?email={email}"
    )
    assert response1.status_code == 200
    
    # Try to unregister again
    response2 = client.delete(
        f"/activities/Programming%20Class/unregister?email={email}"
    )
    
    assert response2.status_code == 400
    assert "detail" in response2.json()
    assert "not signed up" in response2.json()["detail"]


def test_unregister_does_not_affect_other_activities(client):
    """Test that unregistering from one activity doesn't affect others"""
    email = "other@mergington.edu"
    
    # Sign up for two activities
    client.post(f"/activities/Chess%20Club/signup?email={email}")
    client.post(f"/activities/Gym%20Class/signup?email={email}")
    
    # Unregister from Chess Club
    response = client.delete(
        f"/activities/Chess%20Club/unregister?email={email}"
    )
    assert response.status_code == 200
    
    # Verify only Chess Club was affected
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
    assert email in activities["Gym Class"]["participants"]
