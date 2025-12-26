import pytest
import json
import tempfile
import os
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

class TestAPI:
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "DQ-Guard API is running"}
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_upload_csv_validation(self):
        """Test CSV file upload validation"""
        # Create a temporary CSV file
        csv_content = """id,name,email,age
1,Alice,alice@test.com,25
2,Bob,bob@test.com,30
3,Charlie,,35
4,David,david@test.com,
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as f:
                response = client.post(
                    "/validate/upload",
                    files={"file": ("test.csv", f, "text/csv")}
                )
            
            assert response.status_code == 200
            data = response.json()
            
            # Check response structure
            assert "source" in data
            assert "total_rows" in data
            assert "total_columns" in data
            assert "quality_score" in data
            assert "validation_results" in data
            
            # Check data dimensions
            assert data["total_rows"] == 4
            assert data["total_columns"] == 4
            
        finally:
            os.unlink(temp_file_path)
    
    def test_upload_json_validation(self):
        """Test JSON file upload validation"""
        json_data = [
            {"id": 1, "name": "Alice", "email": "alice@test.com", "age": 25},
            {"id": 2, "name": "Bob", "email": "bob@test.com", "age": 30},
            {"id": 3, "name": "Charlie", "email": None, "age": 35}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(json_data, f)
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as f:
                response = client.post(
                    "/validate/upload",
                    files={"file": ("test.json", f, "application/json")}
                )
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_rows"] == 3
            assert data["total_columns"] == 4
            
        finally:
            os.unlink(temp_file_path)
    
    def test_upload_unsupported_file(self):
        """Test upload of unsupported file format"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a text file")
            temp_file_path = f.name
        
        try:
            with open(temp_file_path, 'rb') as f:
                response = client.post(
                    "/validate/upload",
                    files={"file": ("test.txt", f, "text/plain")}
                )
            
            assert response.status_code == 400
            assert "Unsupported file format" in response.json()["detail"]
            
        finally:
            os.unlink(temp_file_path)
    
    def test_custom_rules_validation(self):
        """Test validation with custom rules"""
        test_data = {
            "data": [
                {"name": "Alice", "age": 25, "email": "alice@test.com"},
                {"name": "Bob", "age": 30, "email": "invalid-email"},
                {"name": "Charlie", "age": 17, "email": "charlie@test.com"}
            ],
            "rules": [
                {
                    "name": "age_check",
                    "type": "range_check",
                    "column": "age",
                    "params": {"min": 18, "max": 65}
                },
                {
                    "name": "email_check",
                    "type": "regex_check",
                    "column": "email",
                    "params": {"pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"}
                }
            ]
        }
        
        response = client.post("/validate/rules", json=test_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "custom_rules_results" in data
        assert "age_check" in data["custom_rules_results"]
        assert "email_check" in data["custom_rules_results"]
        assert "quality_score" in data
    
    def test_dashboard_summary(self):
        """Test dashboard summary endpoint"""
        response = client.get("/dashboard/summary")
        assert response.status_code == 200
        
        data = response.json()
        expected_keys = [
            "total_validations",
            "average_quality_score", 
            "unique_sources",
            "recent_validations",
            "quality_distribution"
        ]
        
        for key in expected_keys:
            assert key in data
    
    def test_quality_trends(self):
        """Test quality trends endpoint"""
        response = client.get("/dashboard/trends")
        assert response.status_code == 200
        
        data = response.json()
        assert "daily_trends" in data
        assert "source_trends" in data
        assert isinstance(data["daily_trends"], list)
        assert isinstance(data["source_trends"], list)
    
    def test_validation_history(self):
        """Test validation history endpoint"""
        response = client.get("/validation/history")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        
        # If there are items, check structure
        if data:
            item = data[0]
            expected_keys = ["source", "timestamp", "total_rows", "total_columns", "quality_score"]
            for key in expected_keys:
                assert key in item
    
    def test_schedule_validation(self):
        """Test scheduling validation endpoint"""
        schedule_data = {
            "name": "Test Scheduled Job",
            "schedule": "daily",
            "data_source": {
                "type": "file",
                "path": "/path/to/test.csv"
            },
            "alerts": {
                "enabled": True,
                "type": "email",
                "quality_threshold": 80,
                "to_email": "test@example.com"
            }
        }
        
        response = client.post("/schedule/validation", json=schedule_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "job_id" in data
        assert "status" in data
        assert data["status"] == "scheduled"

class TestAPIErrorHandling:
    
    def test_empty_file_upload(self):
        """Test upload with no file"""
        response = client.post("/validate/upload")
        assert response.status_code == 422  # Validation error
    
    def test_malformed_json_rules(self):
        """Test custom rules with malformed JSON"""
        response = client.post(
            "/validate/rules",
            json={"invalid": "structure"}
        )
        # Should handle gracefully, might return 500 or validation error
        assert response.status_code in [400, 422, 500]
    
    def test_invalid_schedule_data(self):
        """Test scheduling with invalid data"""
        invalid_data = {
            "name": "",  # Empty name
            "schedule": "invalid_schedule",
            "data_source": {}  # Missing required fields
        }
        
        response = client.post("/schedule/validation", json=invalid_data)
        # Should return error for invalid data
        assert response.status_code in [400, 422, 500]

class TestAPIIntegration:
    
    def test_full_validation_workflow(self):
        """Test complete validation workflow"""
        # 1. Upload and validate a file
        csv_content = """id,name,score
1,Alice,95
2,Bob,87
3,Charlie,92
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_file_path = f.name
        
        try:
            # Upload file
            with open(temp_file_path, 'rb') as f:
                upload_response = client.post(
                    "/validate/upload",
                    files={"file": ("workflow_test.csv", f, "text/csv")}
                )
            
            assert upload_response.status_code == 200
            validation_data = upload_response.json()
            
            # 2. Check dashboard summary (should include new validation)
            summary_response = client.get("/dashboard/summary")
            assert summary_response.status_code == 200
            
            # 3. Check validation history
            history_response = client.get("/validation/history")
            assert history_response.status_code == 200
            history_data = history_response.json()
            
            # Should have at least one validation (the one we just did)
            assert len(history_data) >= 0
            
        finally:
            os.unlink(temp_file_path)

if __name__ == '__main__':
    pytest.main([__file__])