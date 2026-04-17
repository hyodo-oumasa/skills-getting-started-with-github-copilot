import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def test_activities():
    """Provide isolated test activities data"""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["alice@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater performances and acting workshops",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 2,
            "participants": []
        }
    }


@pytest.fixture(autouse=True)
def reset_activities(test_activities):
    """Reset activities to test data before each test"""
    activities.clear()
    activities.update(deepcopy(test_activities))
    yield
    # Cleanup after each test
    activities.clear()
