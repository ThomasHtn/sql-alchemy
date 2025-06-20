import pytest
from fastapi.testclient import TestClient

from database import Base, engine
from main import app

client = TestClient(app)


# Setup database
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Client objet to create
def create_sample_client():
    return {
        "age": 35,
        "height_cm": 180.5,
        "weight_kg": 75.2,
        "has_sports_license": True,
        "education_level": 5,
        "region": "Île-de-France",
        "is_smoker": False,
        "estimated_monthly_income": 4200.00,
        "marital_status": "Married",
        "credit_history": "Good",
        "personal_risk_score": 0.2,
        "credit_score": 750,
        "monthly_rent": 950.0,
        "loan_amount_requested": 15000.0,
    }


# =============================
# Test 01 : Add new client
# =============================
def test_create_client():
    response = client.post("/clients/", json=create_sample_client())

    print(response)
    assert response.status_code == 200
    data = response.json()
    assert data["age"] == 35
    assert data["credit_score"] == 750


# =============================
# Test 02 : Get client by id
# =============================
def test_get_client():
    response = client.post("/clients/", json=create_sample_client())
    client_id = response.json()["id"]
    get_response = client.get(f"/clients/{client_id}")
    assert get_response.status_code == 200


# =============================
# Test 03 :  Partial client update
# =============================
def test_update_client():
    # Create client
    create_response = client.post("/clients/", json=create_sample_client())
    assert create_response.status_code == 200
    created_client = create_response.json()
    client_id = created_client["id"]

    # Partial update
    patch_data = {"estimated_monthly_income": 6000, "age": 45}
    patch_response = client.patch(f"/clients/{client_id}", json=patch_data)

    assert patch_response.status_code == 200
    updated_client = patch_response.json()

    # Check for data updated
    assert updated_client["estimated_monthly_income"] == 6000
    assert updated_client["age"] == 45


# =============================
# Test 04 : Delete client by id
# =============================
def test_delete_client():
    post = client.post("/clients/", json=create_sample_client())
    client_id = post.json()["id"]

    delete = client.delete(f"/clients/{client_id}")
    assert delete.status_code == 200
    assert "deleted" in delete.json()["message"]

    get = client.get(f"/clients/{client_id}")
    assert get.status_code == 404
