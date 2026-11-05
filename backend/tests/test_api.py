import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model_mode" in data


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Breed Recognition API" in data["message"]


def test_list_breeds():
    response = client.get("/api/v1/breeds")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 14
    breed_names = [b["name"] for b in data]
    assert "Gir" in breed_names
    assert "Murrah" in breed_names


def test_filter_breeds_by_species():
    cattle_res = client.get("/api/v1/breeds?species=cattle")
    assert cattle_res.status_code == 200
    cattle_data = cattle_res.json()
    assert all(b["species"] == "cattle" for b in cattle_data)

    buffalo_res = client.get("/api/v1/breeds?species=buffalo")
    assert buffalo_res.status_code == 200
    buffalo_data = buffalo_res.json()
    assert all(b["species"] == "buffalo" for b in buffalo_data)


def test_predict_endpoint_valid_image():
    # Create valid synthetic test image
    img = Image.new("RGB", (224, 224), color=(180, 100, 50))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    files = {"file": ("test_cow.jpg", buf, "image/jpeg")}
    response = client.post("/api/v1/predict", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_breed" in data
    assert "confidence" in data
    assert len(data["top_predictions"]) >= 1
    assert data["confidence"] > 0


def test_predict_validation_unsupported_media():
    buf = io.BytesIO(b"fake text file content")
    files = {"file": ("document.txt", buf, "text/plain")}
    response = client.post("/api/v1/predict", files=files)
    assert response.status_code == 415


def test_predict_validation_corrupt_image():
    buf = io.BytesIO(b"corrupt non-image binary data")
    files = {"file": ("corrupt.jpg", buf, "image/jpeg")}
    response = client.post("/api/v1/predict", files=files)
    assert response.status_code == 422

