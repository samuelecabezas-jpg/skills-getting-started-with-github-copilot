"""
Tests for the home/root endpoint.
"""

import pytest


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follows(client):
    """Test that GET / can be followed to static index"""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
