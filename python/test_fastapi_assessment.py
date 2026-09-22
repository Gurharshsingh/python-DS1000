import pytest
from fastapi.testclient import TestClient

# Instructions for the student:
# Create a file named 'student_app.py' in the same directory.
# Inside 'student_app.py', instantiate a FastAPI application named 'app'.
# Implement the endpoints required to pass the tests below.

try:
    from student_app import app
    client = TestClient(app)
except ImportError:
    pytest.skip("student_app.py not found or app not instantiated", allow_module_level=True)


# ==========================================
# Section 1: Concept Tests
# ==========================================

def test_basic_endpoint():
    """
    Concept 1: Basic Routing (like 01_hello_world.py)
    Task: Create a simple GET endpoint at '/health' that returns a status OK message.
    """
    response = client.get("/health")
    assert response.status_code == 200, "Expected status code 200 for /health"
    assert response.json() == {"status": "ok"}, "Expected JSON response {'status': 'ok'}"


def test_pydantic_model_validation():
    """
    Concept 2: Pydantic Models (like 02_pydantic_models.py)
    Task: Create a POST endpoint at '/users' that accepts a JSON body.
    The body must have 'name' (str), 'email' (str), and 'age' (int).
    'email' is required, so missing it should trigger a 422 validation error.
    """
    # Missing 'email' should fail validation
    response_invalid = client.post("/users", json={"name": "Alice", "age": 25})
    assert response_invalid.status_code == 422, "Expected 422 Unprocessable Entity for missing required field"


def test_status_codes():
    """
    Concept 3: Status Codes (like 03_status_codes.py)
    Task: Ensure that querying a non-existent user returns a 404 Not Found 
    status code with a custom error message.
    """
    response = client.get("/users/999999")
    assert response.status_code == 404, "Expected 404 Not Found for non-existent resource"
    assert response.json() == {"detail": "User not found"}, "Expected detail message 'User not found'"


# ==========================================
# Section 2: Integrated Test
# ==========================================

def test_integrated_crud_workflow():
    """
    Concept 4: Integrated Test (combining all concepts + 04_crud_api.py)
    
    Task: Create a complete CRUD lifecycle for a 'Product' resource.
    - POST /products: Create a product (name, price, stock). Returns 201 Created.
    - GET /products/{id}: Retrieve the product. Returns 200 OK.
    - PUT /products/{id}: Update the product. Returns 200 OK.
    - DELETE /products/{id}: Delete the product. Returns 204 No Content (or 200 OK).
    - GET /products/{id}: Attempting to retrieve after deletion should return 404 Not Found.
    """
    
    # 1. Create a Product
    product_payload = {"name": "Mechanical Keyboard", "price": 150.0, "stock": 50}
    create_resp = client.post("/products", json=product_payload)
    assert create_resp.status_code == 201, "Expected 201 Created when a product is successfully created"
    
    created_product = create_resp.json()
    assert "id" in created_product, "Created product response must include an 'id' field"
    product_id = created_product["id"]
    assert created_product["name"] == "Mechanical Keyboard"
    
    # 2. Read the Product
    get_resp = client.get(f"/products/{product_id}")
    assert get_resp.status_code == 200, "Expected 200 OK when retrieving an existing product"
    assert get_resp.json()["id"] == product_id
    
    # 3. Update the Product
    update_payload = {"name": "Wireless Mechanical Keyboard", "price": 180.0, "stock": 45}
    update_resp = client.put(f"/products/{product_id}", json=update_payload)
    assert update_resp.status_code == 200, "Expected 200 OK when updating a product"
    assert update_resp.json()["price"] == 180.0
    
    # 4. Delete the Product
    delete_resp = client.delete(f"/products/{product_id}")
    assert delete_resp.status_code in [200, 204], "Expected 204 No Content (or 200) when deleting a product"
    
    # 5. Verify Deletion (404 Status Code)
    verify_resp = client.get(f"/products/{product_id}")
    assert verify_resp.status_code == 404, "Expected 404 Not Found when retrieving a deleted product"
