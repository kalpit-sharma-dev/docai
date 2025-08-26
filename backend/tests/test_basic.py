import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import init_db, drop_tables
from app.config.settings import settings

# Create test client
client = TestClient(app)

@pytest.fixture(scope="session")
def setup_database():
    """Setup test database."""
    init_db()
    yield
    drop_tables()

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == settings.PROJECT_NAME

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data

def test_api_info():
    """Test API info endpoint."""
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "supported_languages" in data
    assert "supported_stages" in data

def test_supported_languages():
    """Test supported languages endpoint."""
    response = client.get("/api/v1/languages")
    assert response.status_code == 200
    data = response.json()
    assert "supported_languages" in data
    assert "language_names" in data
    assert len(data["supported_languages"]) > 0

def test_processing_stages():
    """Test processing stages endpoint."""
    response = client.get("/api/v1/stages")
    assert response.status_code == 200
    data = response.json()
    assert "stages" in data
    assert len(data["stages"]) == 3
    assert data["stages"][0]["stage"] == 1
    assert data["stages"][1]["stage"] == 2
    assert data["stages"][2]["stage"] == 3

def test_storage_stats():
    """Test storage stats endpoint."""
    response = client.get("/api/v1/storage/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_files" in data
    assert "total_size_bytes" in data
    assert "upload_directory" in data

def test_documents_endpoint():
    """Test documents endpoint."""
    response = client.get("/api/v1/documents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_metrics_endpoint():
    """Test metrics endpoint."""
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "timestamp" in data
    assert "cpu_usage" in data
    assert "memory_usage" in data

def test_invalid_document_status():
    """Test invalid document status endpoint."""
    response = client.get("/api/v1/status/invalid-id")
    assert response.status_code == 404

def test_invalid_document_delete():
    """Test invalid document delete endpoint."""
    response = client.delete("/api/v1/documents/invalid-id")
    assert response.status_code == 404

def test_invalid_document_download():
    """Test invalid document download endpoint."""
    response = client.get("/api/v1/documents/invalid-id/download")
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__])
