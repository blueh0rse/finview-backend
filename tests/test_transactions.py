from fastapi.testclient import TestClient
from src.api.main import app
from src.api.models.transactions import Transaction
import uuid

# must comply with api guidelines

client = TestClient(app)


def test_get_transactions():
    """Test GET /transactions returns 200 and a list of Transactions or empty list"""
    response = client.get("/transactions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Each item should be a valid Transaction
    for item in data:
        transaction = Transaction(**item)
        assert transaction.id
        assert transaction.asset_symbol
        assert transaction.operation in ["buy", "sell"]


def test_get_transactions_with_pagination():
    """Test GET /transactions with pagination parameters"""
    response = client.get("/transactions?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10  # Should respect limit


def test_create_transaction():
    """Test POST /transactions creates a new transaction"""
    # First, create an asset
    asset_data = {
        "symbol": "BTC",
        "name": "Bitcoin",
        "category": "CRYPTO",
        "current_price": 50000.0,
    }
    client.post("/assets", json=asset_data)

    transaction_data = {
        "asset_symbol": "BTC",
        "operation": "buy",
        "amount": 1000.0,
        "quantity": 0.02,
        "unit_price": 50000.0,
        "currency": "USD",
        "date": "2023-01-01T00:00:00Z",
        "comment": "Test transaction",
    }
    response = client.post("/transactions", json=transaction_data)
    assert response.status_code == 201
    created_transaction = response.json()
    # Should return the created transaction
    assert created_transaction["asset_symbol"] == "BTC"
    assert created_transaction["operation"] == "buy"
    assert created_transaction["amount"] == 1000.0
    global test_transaction_id
    test_transaction_id = created_transaction["id"]


def test_get_transaction_by_id():
    """Test GET /transactions/{id} returns 200"""
    response = client.get(f"/transactions/{test_transaction_id}")
    assert response.status_code == 200
    transaction = response.json()
    assert transaction["id"] == test_transaction_id
    assert transaction["asset_symbol"] == "BTC"


def test_get_transaction_not_found():
    """Test GET /transactions/{id} returns 404 for non-existent transaction"""
    fake_id = str(uuid.uuid4())
    response = client.get(f"/transactions/{fake_id}")
    assert response.status_code == 404


def test_get_transactions_invalid_pagination():
    """Test GET /transactions returns 400 for invalid pagination params"""
    # Test negative skip
    response = client.get("/transactions?skip=-1&limit=10")
    assert response.status_code == 400
    # Test zero limit
    response = client.get("/transactions?skip=0&limit=0")
    assert response.status_code == 400
    # Test limit too large (assuming max is 100)
    response = client.get("/transactions?skip=0&limit=101")
    assert response.status_code == 400


def test_create_transaction_invalid_payload():
    """Test POST /transactions returns 422 for invalid payload"""
    # Missing required fields
    transaction_data = {
        "asset_symbol": "BTC",
        "operation": "buy",
        # Missing amount, quantity, etc.
        "currency": "USD",
    }
    response = client.post("/transactions", json=transaction_data)
    assert response.status_code == 422
    # Invalid operation
    transaction_data = {
        "asset_symbol": "BTC",
        "operation": "invalid",
        "amount": 1000.0,
        "quantity": 0.02,
        "unit_price": 50000.0,
        "currency": "USD",
        "date": "2023-01-01T00:00:00Z",
    }
    response = client.post("/transactions", json=transaction_data)
    assert response.status_code == 422


def test_create_transaction_asset_not_found():
    """Test POST /transactions returns 400 for non-existent asset"""
    transaction_data = {
        "asset_symbol": "XYZ",
        "operation": "buy",
        "amount": 1000.0,
        "quantity": 0.02,
        "unit_price": 50000.0,
        "currency": "USD",
        "date": "2023-01-01T00:00:00Z",
    }
    response = client.post("/transactions", json=transaction_data)
    assert response.status_code == 400


def test_update_transaction_success():
    """Test PUT /transactions/{id} updates existing transaction"""
    update_data = {
        "amount": 1500.0,
        "comment": "Updated transaction",
    }
    response = client.put(f"/transactions/{test_transaction_id}", json=update_data)
    assert response.status_code == 200
    updated_transaction = response.json()
    assert updated_transaction["amount"] == 1500.0
    assert updated_transaction["comment"] == "Updated transaction"


def test_update_transaction_not_found():
    """Test PUT /transactions/{id} returns 404 for non-existent transaction"""
    fake_id = str(uuid.uuid4())
    update_data = {
        "amount": 2000.0,
    }
    response = client.put(f"/transactions/{fake_id}", json=update_data)
    assert response.status_code == 404


def test_update_transaction_invalid_payload():
    """Test PUT /transactions/{id} returns 422 for invalid payload"""
    update_data = {
        "operation": "invalid",
    }
    response = client.put(f"/transactions/{test_transaction_id}", json=update_data)
    assert response.status_code == 422


def test_delete_transaction_success():
    """Test DELETE /transactions/{id} deletes existing transaction"""
    response = client.delete(f"/transactions/{test_transaction_id}")
    assert response.status_code == 204
    # Verify it's gone
    response = client.get(f"/transactions/{test_transaction_id}")
    assert response.status_code == 404


def test_delete_transaction_not_found():
    """Test DELETE /transactions/{id} returns 404 for non-existent transaction"""
    fake_id = str(uuid.uuid4())
    response = client.delete(f"/transactions/{fake_id}")
    assert response.status_code == 404
