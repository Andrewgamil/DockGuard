import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from main import app, get_session
from models import Link

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def get_test_session():
    with Session(test_engine) as session:
        yield session

@pytest.fixture(scope="function")
def client():
    # Create test database
    SQLModel.metadata.create_all(test_engine)
    
    # Override dependency
    app.dependency_overrides[get_session] = get_test_session
    
    yield TestClient(app)
    
    # Cleanup
    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(test_engine)

def test_shorten_url(client):
    """Test URL shortening endpoint"""
    response = client.post(
        "/shorten",
        json={"url": "https://example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert len(data["short_code"]) > 0

def test_shorten_url_invalid(client):
    """Test URL shortening with invalid URL"""
    response = client.post(
        "/shorten",
        json={"url": "not-a-url"}
    )
    assert response.status_code == 400

def test_redirect_url(client):
    """Test URL redirect"""
    # First create a short URL
    create_response = client.post(
        "/shorten",
        json={"url": "https://example.com"}
    )
    short_code = create_response.json()["short_code"]
    
    # Then redirect
    redirect_response = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_response.status_code == 302
    assert redirect_response.headers["location"] == "https://example.com"

def test_redirect_404(client):
    """Test redirect with non-existent short code"""
    response = client.get("/nonexistent123", follow_redirects=False)
    assert response.status_code == 404

def test_metrics_endpoint(client):
    """Test metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "urlshort_created_total" in response.text
    assert "urlshort_redirects_total" in response.text
    assert "urlshort_404_total" in response.text

