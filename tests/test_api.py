"""
Comprehensive API endpoint tests
Run with: pytest tests/test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# SET TESTING ENVIRONMENT VARIABLE BEFORE IMPORTING APP
os.environ["TESTING"] = "true"

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.server import app, get_db
from database.models import Base

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test database
Base.metadata.drop_all(bind=engine)  # Clear any existing data
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# ============================================
# SHARED TEST DATA (Module Level)
# ============================================

TEST_USER_EMAIL = "test_user@example.com"
TEST_USER_API_KEY = None
TEST_JOB_ID = None

# ============================================
# TEST CLASSES
# ============================================

class TestAuthentication:
    """Test authentication and user management"""
    
    def test_01_signup_success(self):
        """Test successful user signup"""
        global TEST_USER_API_KEY
        
        response = client.post(
            "/signup",
            json={"email": TEST_USER_EMAIL}
        )
        assert response.status_code == 200
        data = response.json()
        assert "api_key" in data
        assert data["email"] == TEST_USER_EMAIL
        assert data["subscription_tier"] == "free"
        
        # Store API key for other tests
        TEST_USER_API_KEY = data["api_key"]
        print(f"\n✅ Created test user with API key: {TEST_USER_API_KEY[:20]}...")
    
    def test_02_signup_duplicate_email(self):
        """Test signup with duplicate email fails"""
        response = client.post(
            "/signup",
            json={"email": TEST_USER_EMAIL}
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()
    
    def test_03_signup_invalid_email(self):
        """Test signup with invalid email fails"""
        response = client.post(
            "/signup",
            json={"email": "not-an-email"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_04_signup_new_user(self):
        """Test creating another user works"""
        response = client.post(
            "/signup",
            json={"email": "another_user@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "api_key" in data
        print(f"✅ Created another user: {data['email']}")


class TestContentGeneration:
    """Test content generation endpoints"""
    
    def test_01_generate_without_auth(self):
        """Test generate endpoint without API key fails"""
        response = client.post(
            "/generate",
            json={"topic": "Test Topic"}
        )
        assert response.status_code == 401
        assert "API Key required" in response.json()["detail"]
    
    def test_02_generate_with_invalid_api_key(self):
        """Test generate endpoint with invalid API key fails"""
        response = client.post(
            "/generate",
            json={"topic": "Test Topic"},
            headers={"X-API-Key": "invalid_key_12345"}
        )
        assert response.status_code == 403
        assert "Invalid API Key" in response.json()["detail"]
    
    def test_03_generate_success(self):
        """Test successful content generation"""
        global TEST_JOB_ID
        
        assert TEST_USER_API_KEY is not None, "Test user must be created first"
        
        response = client.post(
            "/generate",
            json={"topic": "AI in Healthcare"},
            headers={"X-API-Key": TEST_USER_API_KEY}
        )
        
        print(f"\n📝 Generate response status: {response.status_code}")
        print(f"📝 Generate response: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "processing"
        assert "usage" in data
        
        # Store job_id for other tests
        TEST_JOB_ID = data["job_id"]
        print(f"✅ Generated job_id: {TEST_JOB_ID}")
    
    def test_04_generate_empty_topic(self):
        """Test generate with empty topic fails"""
        assert TEST_USER_API_KEY is not None, "Test user must be created first"
        
        response = client.post(
            "/generate",
            json={"topic": ""},
            headers={"X-API-Key": TEST_USER_API_KEY}
        )
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_05_generate_too_long_topic(self):
        """Test generate with too long topic fails"""
        assert TEST_USER_API_KEY is not None, "Test user must be created first"
        
        long_topic = "A" * 201  # 201 characters
        response = client.post(
            "/generate",
            json={"topic": long_topic},
            headers={"X-API-Key": TEST_USER_API_KEY}
        )
        assert response.status_code == 400
        assert "200 characters" in response.json()["detail"].lower()
    
    def test_06_status_check(self):
        """Test job status endpoint"""
        assert TEST_USER_API_KEY is not None, "Test user must be created first"
        assert TEST_JOB_ID is not None, "Job must be created first"
        
        response = client.get(
            f"/status/{TEST_JOB_ID}",
            headers={"X-API-Key": TEST_USER_API_KEY}
        )
        
        print(f"\n📊 Status response: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == TEST_JOB_ID
        assert "status" in data
        assert data["status"] in ["processing", "completed", "failed"]
    
    def test_07_status_check_invalid_job(self):
        """Test status check with invalid job_id"""
        assert TEST_USER_API_KEY is not None, "Test user must be created first"
        
        response = client.get(
            "/status/invalid-job-id-12345",
            headers={"X-API-Key": TEST_USER_API_KEY}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_08_status_check_without_auth(self):
        """Test status check without authentication"""
        assert TEST_JOB_ID is not None, "Job must be created first"
        
        response = client.get(f"/status/{TEST_JOB_ID}")
        assert response.status_code == 401


class TestUsageTracking:
    """Test usage tracking and limits"""
    
    def test_01_usage_endpoint(self):
        """Test usage statistics endpoint"""
        assert TEST_USER_API_KEY is not None, "Test user must be created first"
        
        response = client.get(
            "/usage",
            headers={"X-API-Key": TEST_USER_API_KEY}
        )
        assert response.status_code == 200
        data = response.json()
        assert "usage_count" in data
        assert "monthly_limit" in data
        assert "remaining" in data
        assert data["email"] == TEST_USER_EMAIL
        print(f"\n📊 Usage: {data['usage_count']}/{data['monthly_limit']}")
    
    def test_02_usage_without_auth(self):
        """Test usage endpoint without authentication"""
        response = client.get("/usage")
        assert response.status_code == 401


class TestSystemEndpoints:
    """Test system and admin endpoints"""
    
    def test_01_health_check(self):
        """Test health check endpoint (no auth required)"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert data["status"] in ["healthy", "degraded"]
        print(f"\n💚 Health: {data['status']}")
    
    def test_02_admin_stats(self):
        """Test admin statistics endpoint"""
        response = client.get("/admin/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "total_jobs" in data
        assert "success_rate" in data
        print(f"\n📊 Platform stats: {data}")
    
    def test_03_admin_costs(self):
        """Test admin cost analytics endpoint"""
        response = client.get("/admin/costs")
        assert response.status_code == 200
        data = response.json()
        assert "total_cost" in data
        assert "avg_cost_per_job" in data
        print(f"\n💰 Costs: {data}")


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_01_invalid_endpoint(self):
        """Test non-existent endpoint returns 404"""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_02_invalid_http_method(self):
        """Test invalid HTTP method"""
        response = client.get("/generate")  # Should be POST
        assert response.status_code == 405
    
    def test_03_malformed_json(self):
        """Test malformed JSON body"""
        assert TEST_USER_API_KEY is not None, "Test user must be created first"
        
        response = client.post(
            "/generate",
            data="this is not json",  # Invalid JSON
            headers={
                "X-API-Key": TEST_USER_API_KEY,
                "Content-Type": "application/json"
            }
        )
        assert response.status_code == 422


# ============================================
# PYTEST CONFIGURATION
# ============================================

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup test database after all tests"""
    def remove_test_db():
        import os
        if os.path.exists("test.db"):
            os.remove("test.db")
            print("\n🗑️  Cleaned up test database")
    
    request.addfinalizer(remove_test_db)


def pytest_configure(config):
    """Configure pytest"""
    # Ensure tests run in order
    config.addinivalue_line(
        "markers", "order: mark test execution order"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])