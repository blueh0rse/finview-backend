from datetime import datetime, timedelta, timedelta
import random
import uuid
from fastapi.testclient import TestClient
from src.api.main import app
from src.api.models.assets import Asset

# Tests for Assets endpoints
# These tests include both "guideline expectations" (what the API SHOULD do per
# `private/API_guidelines.md`) and tests that assert the current behavior of
# the implementation so mismatches are obvious.

client = TestClient(app)


def unique_symbol(base: str) -> str:
    # produce a short unique symbol (2-10 uppercase letters)
    return (base + str(uuid.uuid4().hex[:4])).upper()[:10]


def test_create_asset():
    """Test creating a new asset"""
    symbol = unique_symbol("T")
    asset_data = {
        "symbol": symbol,
        "name": "Test Asset",
        "category": "CRYPTO",
        "current_price": 50000.0,
    }

    print(asset_data)

    response = client.post("/assets", json=asset_data)
    assert response.status_code == 201
    created_asset = response.json()
    assert created_asset["symbol"] == symbol
    assert created_asset["name"] == "Test Asset"
    assert created_asset["category"] == "CRYPTO"
    assert created_asset["current_price"] == 50000.0


def test_get_asset():
    """Test retrieving a specific asset by symbol"""
    # First create an asset
    symbol = unique_symbol("BTC")
    asset_data = {
        "symbol": symbol,
        "name": "Bitcoin",
        "category": "CRYPTO",
        "current_price": 60000.0,
        "updated_at": datetime.now().isoformat()
    }
    create_response = client.post("/assets", json=asset_data)
    assert create_response.status_code == 201

    # Now get it
    response = client.get(f"/assets/{symbol}")
    assert response.status_code == 200
    asset = response.json()
    assert asset["symbol"] == symbol
    assert asset["name"] == "Bitcoin"


def test_get_asset_not_found():
    """Test getting a non-existent asset returns 404"""
    response = client.get("/assets/NONEXISTENT")
    assert response.status_code == 404


def test_get_all_assets():
    """Test retrieving all assets"""
    # Create a few assets first
    symbols = []
    for i in range(3):
        symbol = unique_symbol(f"ASSET{i}")
        asset_data = {
            "symbol": symbol,
            "name": f"Asset {i}",
            "category": "STOCK",
            "current_price": 100.0 + i * 10,
            "updated_at": datetime.now().isoformat()
        }
        response = client.post("/assets", json=asset_data)
        assert response.status_code == 201
        symbols.append(symbol)

    # Get all assets
    response = client.get("/assets")
    assert response.status_code == 200
    assets = response.json()
    assert isinstance(assets, list)
    # Should contain at least the assets we created
    asset_symbols = [asset["symbol"] for asset in assets]
    for symbol in symbols:
        assert symbol in asset_symbols


def test_update_asset():
    """Test updating an existing asset"""
    # Create an asset
    symbol = unique_symbol("UPDATE")
    asset_data = {
        "symbol": symbol,
        "name": "Original Name",
        "category": "CRYPTO",
        "current_price": 40000.0,
        "updated_at": datetime.now().isoformat()
    }
    create_response = client.post("/assets", json=asset_data)
    assert create_response.status_code == 201

    # Update it
    update_data = {
        "symbol": symbol,  # Same symbol
        "name": "Updated Name",
        "category": "CRYPTO",
        "current_price": 45000.0,
        "updated_at": datetime.now().isoformat()
    }
    response = client.put(f"/assets/{symbol}", json=update_data)
    assert response.status_code == 200
    updated_asset = response.json()
    assert updated_asset["name"] == "Updated Name"
    assert updated_asset["current_price"] == 45000.0


def test_update_asset_not_found():
    """Test updating a non-existent asset returns 404"""
    update_data = {
        "symbol": "NONEXISTENT",
        "name": "Doesn't Matter",
        "category": "CRYPTO",
        "current_price": 1000.0,
        "updated_at": datetime.now().isoformat()
    }
    response = client.put("/assets/NONEXISTENT", json=update_data)
    assert response.status_code == 404


def test_delete_asset():
    """Test deleting an asset"""
    # Create an asset
    symbol = unique_symbol("DELETE")
    asset_data = {
        "symbol": symbol,
        "name": "To Be Deleted",
        "category": "BOND",
        "current_price": 1000.0,
        "updated_at": datetime.now().isoformat()
    }
    create_response = client.post("/assets", json=asset_data)
    assert create_response.status_code == 201

    # Delete it
    response = client.delete(f"/assets/{symbol}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = client.get(f"/assets/{symbol}")
    assert get_response.status_code == 404


def test_delete_asset_not_found():
    """Test deleting a non-existent asset returns 404"""
    response = client.delete("/assets/NONEXISTENT")
    assert response.status_code == 404


def test_create_asset_duplicate_symbol():
    """Test creating an asset with duplicate symbol returns 400"""
    symbol = unique_symbol("DUPE")
    asset_data = {
        "symbol": symbol,
        "name": "First Asset",
        "category": "STOCK",
        "current_price": 100.0,
        "updated_at": datetime.now().isoformat()
    }
    # Create first
    response1 = client.post("/assets", json=asset_data)
    assert response1.status_code == 201

    # Try to create duplicate
    asset_data["name"] = "Second Asset"
    response2 = client.post("/assets", json=asset_data)
    assert response2.status_code == 400


