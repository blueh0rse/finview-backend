from fastapi.testclient import TestClient
from src.api.main import app
from src.api.models.assets import Asset

# must comply with api guidelines

client = TestClient(app)


def test_get_assets():
    """Test GET /assets returns 200 and a list of Assets or empty list"""
    response = client.get("/assets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Each item should be a valid Asset
    for item in data:
        asset = Asset(**item)
        assert asset.symbol
        assert asset.name
        assert asset.category

def test_get_assets_with_pagination():
    """Test GET /assets with pagination parameters"""
    response = client.get("/assets?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10  # Should respect limit
