from datetime import datetime
import uuid
from fastapi.testclient import TestClient
from src.api.main import app

# List of tests:
# - create and get a transaction
# - get all transactions
# - update a transaction (idempotency)
# - delete a transaction
# - get non-existent transaction
# - create invalid transaction


client = TestClient(app)


def test_create_and_get_transaction():
    # Test creating a transaction
    transaction_data = {
        "asset": "BTC",
        "operation": "buy",
        "amount": 1000.0,
        "quantity": 0.05,
        "unit_price": 20000.0,
        "currency": "USD",
        "date": datetime.now().isoformat(),
        "comment": "Test transaction",
    }

    response = client.post("/transactions", json=transaction_data)
    assert response.status_code == 201
    created_transaction = response.json()
    assert created_transaction["asset"] == transaction_data["asset"]
    transaction_id = created_transaction["id"]

    # Test getting the created transaction
    response = client.get(f"/transactions/{transaction_id}")
    assert response.status_code == 200
    assert response.json() == created_transaction


def test_get_all_transactions():
    response = client.get("/transactions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_transaction():
    # First create a transaction
    transaction_data = {
        "asset": "ETH",
        "operation": "buy",
        "amount": 500.0,
        "quantity": 0.3,
        "unit_price": 1666.67,
        "currency": "USD",
        "date": datetime.now().isoformat(),
        "comment": "Original transaction",
    }

    response = client.post("/transactions", json=transaction_data)
    assert response.status_code == 201
    transaction_id = response.json()["id"]

    # Test update
    update_data = {
        "amount": 600.0,
        "quantity": 0.35,
        "unit_price": 1714.29,
        "comment": "Updated transaction",
    }

    # First update
    response = client.put(f"/transactions/{transaction_id}", json=update_data)
    assert response.status_code == 200
    updated_transaction = response.json()
    assert updated_transaction["amount"] == update_data["amount"]
    assert updated_transaction["quantity"] == update_data["quantity"]
    assert updated_transaction["comment"] == update_data["comment"]
    first_update_response = response.json()

    # Second identical update (testing idempotency)
    response = client.put(f"/transactions/{transaction_id}", json=update_data)
    assert response.status_code == 200
    assert response.json() == first_update_response


def test_delete_transaction():
    # First create a transaction
    transaction_data = {
        "asset": "SOL",
        "operation": "sell",
        "amount": 200.0,
        "quantity": 10.0,
        "unit_price": 20.0,
        "currency": "USD",
        "date": datetime.now().isoformat(),
    }

    response = client.post("/transactions", json=transaction_data)
    assert response.status_code == 201
    transaction_id = response.json()["id"]

    # Test deletion
    response = client.delete(f"/transactions/{transaction_id}")
    assert response.status_code == 204

    # Verify the transaction is gone
    response = client.get(f"/transactions/{transaction_id}")
    assert response.status_code == 404


def test_transaction_not_found():
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/transactions/{non_existent_id}")
    assert response.status_code == 404

    response = client.put(f"/transactions/{non_existent_id}", json={"amount": 100.0})
    assert response.status_code == 404

    response = client.delete(f"/transactions/{non_existent_id}")
    assert response.status_code == 404


def test_invalid_transaction_data():
    # Test with invalid operation
    invalid_data = {
        "asset": "BTC",
        "operation": "invalid",  # only 'buy' or 'sell' allowed
        "amount": 1000.0,
        "quantity": 0.05,
        "unit_price": 20000.0,
        "currency": "USD",
        "date": datetime.now().isoformat(),
    }
    response = client.post("/transactions", json=invalid_data)
    assert response.status_code == 422

    # Test with missing required field
    invalid_data = {
        "asset": "BTC",
        "operation": "buy",
        # amount is missing
        "quantity": 0.05,
        "unit_price": 20000.0,
        "currency": "USD",
        "date": datetime.now().isoformat(),
    }
    response = client.post("/transactions", json=invalid_data)
    assert response.status_code == 422
