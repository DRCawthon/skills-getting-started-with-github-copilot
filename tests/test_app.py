"""
Unit tests for the Mergington High School API endpoints.
"""
import sys
import os
import copy
import pytest
from fastapi.testclient import TestClient

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import app, activities

# Create a test client
client = TestClient(app)

# Store the original activities data for test isolation
original_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities data before each test."""
    global activities
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


def test_root_redirect():
    """Test the root endpoint redirects to the static index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    """Test retrieving all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    assert response.json() == original_activities


def test_signup_for_activity_success():
    """Test successfully signing up for an activity."""
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up test@mergington.edu for Chess Club"}
    
    # Verify the student was actually added
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity():
    """Test signing up for an activity that doesn't exist."""
    response = client.post("/activities/Nonexistent Club/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_drop_activity_success():
    """Test successfully dropping from an activity."""
    # First, add a test student to an activity
    activities["Chess Club"]["participants"].append("dropout@mergington.edu")
    
    # Now drop the student from the activity
    response = client.post("/activities/Chess Club/drop?email=dropout@mergington.edu")
    assert response.status_code == 200
    assert response.json() == {"message": "Dropped dropout@mergington.edu from Chess Club"}
    
    # Verify the student was actually removed
    assert "dropout@mergington.edu" not in activities["Chess Club"]["participants"]


def test_drop_from_nonexistent_activity():
    """Test dropping from an activity that doesn't exist."""
    response = client.post("/activities/Nonexistent Club/drop?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_drop_when_not_enrolled():
    """Test dropping from an activity when not enrolled."""
    response = client.post("/activities/Chess Club/drop?email=notenrolled@mergington.edu")
    assert response.status_code == 400
    assert "not enrolled" in response.json()["detail"]


def test_multiple_signups_same_student():
    """Test a student signing up for multiple activities."""
    # Sign up for first activity
    response1 = client.post("/activities/Chess Club/signup?email=multi@mergington.edu")
    assert response1.status_code == 200
    
    # Sign up for second activity
    response2 = client.post("/activities/Programming Class/signup?email=multi@mergington.edu")
    assert response2.status_code == 200
    
    # Verify student is enrolled in both activities
    assert "multi@mergington.edu" in activities["Chess Club"]["participants"]
    assert "multi@mergington.edu" in activities["Programming Class"]["participants"]


def test_signup_then_drop():
    """Test a student signing up and then dropping from an activity."""
    # First, sign up the student
    client.post("/activities/Programming Class/signup?email=signthendrop@mergington.edu")
    
    # Verify student is enrolled
    assert "signthendrop@mergington.edu" in activities["Programming Class"]["participants"]
    
    # Now drop the student
    response = client.post("/activities/Programming Class/drop?email=signthendrop@mergington.edu")
    assert response.status_code == 200
    
    # Verify student is no longer enrolled
    assert "signthendrop@mergington.edu" not in activities["Programming Class"]["participants"]