import pytest
from src.app import is_student_signed_up


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        # Arrange
        expected_activities = ["Chess Club", "Drama Club"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert list(data.keys()) == expected_activities
        assert data["Chess Club"]["max_participants"] == 2
        assert len(data["Drama Club"]["participants"]) == 0


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_student_success(self, client):
        # Arrange
        activity = "Drama Club"
        email = "bob@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        assert email in activities_response.json()["Drama Club"]["participants"]
    
    def test_signup_duplicate_student_fails(self, client):
        # Arrange
        activity = "Chess Club"
        email = "alice@mergington.edu"  # Already signed up
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_fails(self, client):
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""
    
    def test_unregister_existing_participant_success(self, client):
        # Arrange
        activity = "Chess Club"
        email = "alice@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        assert email not in activities_response.json()["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_participant_fails(self, client):
        # Arrange
        activity = "Drama Club"
        email = "notexist@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_from_nonexistent_activity_fails(self, client):
        # Arrange
        activity = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestIsStudentSignedUp:
    """Unit tests for is_student_signed_up function"""
    
    def test_is_student_signed_up_returns_true_for_signed_up_student(self):
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"
        
        # Act
        result = is_student_signed_up(activity_name, email)
        
        # Assert
        assert result is True
    
    def test_is_student_signed_up_returns_false_for_non_signed_up_student(self):
        # Arrange
        activity_name = "Chess Club"
        email = "unknown@mergington.edu"
        
        # Act
        result = is_student_signed_up(activity_name, email)
        
        # Assert
        assert result is False
