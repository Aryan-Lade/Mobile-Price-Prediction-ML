import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

SAMPLE_SMARTPHONE = {
    "brand_name": "samsung",
    "rating": 84.0,
    "has_5g": True,
    "has_nfc": True,
    "has_ir_blaster": False,
    "processor_brand": "snapdragon",
    "num_cores": 8.0,
    "processor_speed": 3.2,
    "battery_capacity": 5000.0,
    "fast_charging_available": 1,
    "fast_charging": 45.0,
    "ram_capacity": 12.0,
    "internal_memory": 256.0,
    "screen_size": 6.8,
    "refresh_rate": 120,
    "resolution": "1440 x 3088",
    "num_rear_cameras": 4,
    "num_front_cameras": 1.0,
    "os": "android",
    "primary_camera_rear": 200.0,
    "primary_camera_front": 12.0,
    "extended_memory_available": 0,
    "extended_upto": 0.0
}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    if "application/json" in response.headers.get("content-type", ""):
        assert "SmartPrice" in response.json()["message"]
    else:
        assert "html" in response.headers.get("content-type", "").lower()


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Random Forest" in data["champion_model"]


def test_predict_single():
    response = client.post("/api/predict", json=SAMPLE_SMARTPHONE)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_category" in data
    assert data["predicted_category"] in ["Budget", "Mid-Range", "Premium", "Flagship"]
    assert len(data["probabilities"]) == 4
    assert "engineered_features" in data
    assert data["engineered_features"]["ppi"] > 0


def test_predict_compare():
    response = client.post("/api/predict/compare", json=SAMPLE_SMARTPHONE)
    assert response.status_code == 200
    data = response.json()
    assert "models_comparison" in data
    assert len(data["models_comparison"]) == 4
    assert "consensus_category" in data


def test_predict_batch():
    batch_payload = {"smartphones": [SAMPLE_SMARTPHONE, SAMPLE_SMARTPHONE]}
    response = client.post("/api/predict/batch", json=batch_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_samples"] == 2
    assert len(data["predictions"]) == 2


def test_models_list():
    response = client.get("/api/models/list")
    assert response.status_code == 200
    data = response.json()
    assert len(data["models"]) == 4
    assert data["champion"] == "random_forest"


def test_models_metrics():
    response = client.get("/api/models/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "champion_model" in data


def test_models_roc_curves():
    response = client.get("/api/models/roc-curves")
    assert response.status_code == 200
    data = response.json()
    assert "models_evaluation" in data
    assert "random_forest" in data["models_evaluation"]


def test_models_feature_importance():
    response = client.get("/api/models/feature-importance")
    assert response.status_code == 200
    data = response.json()
    assert "ranked_features" in data
    assert len(data["ranked_features"]) > 0


def test_analytics_dataset_summary():
    response = client.get("/api/analytics/dataset-summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_rows"] == 980


def test_analytics_eda_insights():
    response = client.get("/api/analytics/eda-insights")
    assert response.status_code == 200
    data = response.json()
    assert "anova_by_price_category" in data


if __name__ == "__main__":
    print("Running API Integration Tests...")
    test_root()
    print("  [OK] Root Endpoint OK")
    test_health()
    print("  [OK] Health Endpoint OK")
    test_predict_single()
    print("  [OK] Single Prediction Endpoint OK")
    test_predict_compare()
    print("  [OK] Model Comparison Endpoint OK")
    test_predict_batch()
    print("  [OK] Batch Prediction Endpoint OK")
    test_models_list()
    print("  [OK] Models List Endpoint OK")
    test_models_metrics()
    print("  [OK] Model Metrics Endpoint OK")
    test_models_roc_curves()
    print("  [OK] ROC Curves Endpoint OK")
    test_models_feature_importance()
    print("  [OK] Feature Importance Endpoint OK")
    test_analytics_dataset_summary()
    print("  [OK] Dataset Summary Endpoint OK")
    test_analytics_eda_insights()
    print("  [OK] EDA Insights Endpoint OK")
    print("\nALL 10 API INTEGRATION TESTS PASSED PERFECTLY!")
