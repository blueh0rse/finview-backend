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


def test_create_asset():
    """Test POST /assets creates a new asset"""
    asset_data = {
        "symbol": "BTC",
        "name": "Bitcoin",
        "category": "CRYPTO",
        "current_price": 50000.0,
    }
    response = client.post("/assets", json=asset_data)
    print(response.json())
    assert response.status_code == 201
    created_asset = response.json()
    # Should return the created asset
    assert created_asset["symbol"] == "BTC"
    assert created_asset["name"] == "Bitcoin"
    assert created_asset["category"] == "CRYPTO"
    assert created_asset["current_price"] == 50000.0


def test_get_asset_by_symbol():
    response = client.get("/assets/btc")
    assert response.status_code == 200
    asset = response.json()
    assert asset["symbol"] == "BTC"
    assert asset["name"] == "Bitcoin"
    assert asset["category"] == "CRYPTO"
    assert asset["current_price"] == 50000.0


def test_get_asset_not_found():
    """Test GET /assets/{symbol} returns 404 for non-existent asset"""
    response = client.get("/assets/NONEXISTENT")
    assert response.status_code == 404


def test_get_assets_invalid_pagination():
    """Test GET /assets returns 400 for invalid pagination params"""
    # Test negative skip
    response = client.get("/assets?skip=-1&limit=10")
    assert response.status_code == 400
    # Test zero limit
    response = client.get("/assets?skip=0&limit=0")
    assert response.status_code == 400
    # Test limit too large (assuming max is 100)
    response = client.get("/assets?skip=0&limit=101")
    assert response.status_code == 400


def test_create_asset_duplicate_symbol():
    """Test POST /assets returns 409 for duplicate symbol"""
    # First, ensure BTC exists (from previous test)
    asset_data = {
        "symbol": "BTC",
        "name": "Bitcoin Duplicate",
        "category": "CRYPTO",
        "current_price": 50000.0,
    }
    response = client.post("/assets", json=asset_data)
    assert response.status_code == 409


def test_create_asset_invalid_payload():
    """Test POST /assets returns 422 for invalid payload"""
    # Missing required fields
    asset_data = {
        "symbol": "ETH",
        # Missing name and category
        "current_price": 3000.0,
    }
    response = client.post("/assets", json=asset_data)
    assert response.status_code == 422
    # Invalid category
    asset_data = {
        "symbol": "ETH",
        "name": "Ethereum",
        "category": "INVALID!",
        "current_price": 3000.0,
    }
    response = client.post("/assets", json=asset_data)
    assert response.status_code == 422


def test_update_asset_success():
    """Test PUT /assets/{symbol} updates existing asset"""
    update_data = {
        "symbol": "BTC",
        "name": "Bitcoin Updated",
        "category": "CRYPTO",
        "current_price": 60000.0,
    }
    response = client.put("/assets/btc", json=update_data)
    assert response.status_code == 200
    updated_asset = response.json()
    assert updated_asset["name"] == "Bitcoin Updated"
    assert updated_asset["current_price"] == 60000.0


def test_update_asset_not_found():
    """Test PUT /assets/{symbol} returns 404 for non-existent asset"""
    update_data = {
        "symbol": "XYZ",
        "name": "Non Existent",
        "category": "STOCK",
    }
    response = client.put("/assets/XYZ", json=update_data)
    assert response.status_code == 404


def test_update_asset_invalid_payload():
    """Test PUT /assets/{symbol} returns 422 for invalid payload"""
    update_data = {
        "symbol": "BTC",
        "name": "",  # Invalid empty name
        "category": "CRYPTO",
    }
    response = client.put("/assets/btc", json=update_data)
    assert response.status_code == 422


def test_update_asset_conflict():
    """Test PUT /assets/{symbol} returns 409 for symbol conflict"""
    # Create another asset first
    asset_data = {
        "symbol": "ETH",
        "name": "Ethereum",
        "category": "CRYPTO",
        "current_price": 3000.0,
    }
    client.post("/assets", json=asset_data)
    # Try to update BTC to ETH
    update_data = {
        "symbol": "ETH",
        "name": "Bitcoin Renamed",
        "category": "CRYPTO",
    }
    response = client.put("/assets/btc", json=update_data)
    assert response.status_code == 409  # Assuming routes handle AssetConflictError


def test_delete_asset_success():
    """Test DELETE /assets/{symbol} deletes existing asset"""
    response = client.delete("/assets/btc")
    assert response.status_code == 204
    # Verify it's gone
    response = client.get("/assets/btc")
    assert response.status_code == 404


def test_delete_asset_not_found():
    """Test DELETE /assets/{symbol} returns 404 for non-existent asset"""
    response = client.delete("/assets/XYZ")
    assert response.status_code == 404
