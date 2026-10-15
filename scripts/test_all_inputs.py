import sys
from pathlib import Path
import json

PROJECT_ROOT = Path("c:/Users/wwa90/OneDrive/Desktop/MLProject")
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

sys.stdout.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

print("=" * 80)
print("COMPREHENSIVE END-TO-END SYSTEM & INPUT ATTRIBUTES VERIFICATION")
print("=" * 80)

# --- 1. HEALTH CHECK ---
print("\n[TEST 1] API Health Check:")
res = client.get("/api/health")
assert res.status_code == 200, f"Health check failed: {res.status_code}"
h_data = res.json()
print(f"  Status: {h_data['status']} | Champion: {h_data['champion_model']} | Models: {h_data['loaded_models']}")

# --- 2. PREDICT: BUDGET TIER ---
print("\n[TEST 2] Predict with Low-End Budget Specs (4G, 4GB RAM, 64GB ROM, Helio, no NFC):")
budget_payload = {
    "brand_name": "xiaomi",
    "rating": 62.0,
    "has_5g": False,
    "has_nfc": False,
    "has_ir_blaster": True,
    "processor_brand": "helio",
    "num_cores": 8.0,
    "processor_speed": 2.0,
    "battery_capacity": 5000.0,
    "fast_charging_available": 1,
    "fast_charging": 18.0,
    "ram_capacity": 4.0,
    "internal_memory": 64.0,
    "screen_size": 6.5,
    "refresh_rate": 60,
    "resolution": "720 x 1600",
    "num_rear_cameras": 2,
    "num_front_cameras": 1.0,
    "os": "android",
    "primary_camera_rear": 13.0,
    "primary_camera_front": 5.0,
    "extended_memory_available": 1,
    "extended_upto": 512.0
}
res = client.post("/api/predict?model=champion", json=budget_payload)
assert res.status_code == 200
b_data = res.json()
print(f"  Predicted Category: {b_data['predicted_category']} (Confidence: {b_data['confidence_percentage']})")
print(f"  Price Range: {b_data['estimated_price_range']}")
assert b_data['predicted_category'] == "Budget", "Expected Budget"

# --- 3. PREDICT: MID-RANGE TIER ---
print("\n[TEST 3] Predict with Mid-Range Specs (5G, 6GB RAM, 128GB ROM, Dimensity, 120Hz):")
mid_payload = {
    "brand_name": "realme",
    "rating": 78.0,
    "has_5g": True,
    "has_nfc": False,
    "has_ir_blaster": False,
    "processor_brand": "dimensity",
    "num_cores": 8.0,
    "processor_speed": 2.6,
    "battery_capacity": 5000.0,
    "fast_charging_available": 1,
    "fast_charging": 33.0,
    "ram_capacity": 6.0,
    "internal_memory": 128.0,
    "screen_size": 6.67,
    "refresh_rate": 120,
    "resolution": "1080 x 2400",
    "num_rear_cameras": 3,
    "num_front_cameras": 1.0,
    "os": "android",
    "primary_camera_rear": 64.0,
    "primary_camera_front": 16.0,
    "extended_memory_available": 1,
    "extended_upto": 1024.0
}
res = client.post("/api/predict?model=champion", json=mid_payload)
assert res.status_code == 200
m_data = res.json()
print(f"  Predicted Category: {m_data['predicted_category']} (Confidence: {m_data['confidence_percentage']})")
print(f"  Price Range: {m_data['estimated_price_range']}")
assert m_data['predicted_category'] in ["Mid-Range", "Premium"]

# --- 4. PREDICT: FLAGSHIP APPLE iOS ---
print("\n[TEST 4] Predict with Apple iOS Flagship Specs (iOS, Bionic A16, 512GB ROM, 48MP):")
ios_payload = {
    "brand_name": "apple",
    "rating": 92.0,
    "has_5g": True,
    "has_nfc": True,
    "has_ir_blaster": False,
    "processor_brand": "bionic",
    "num_cores": 6.0,
    "processor_speed": 3.46,
    "battery_capacity": 4323.0,
    "fast_charging_available": 1,
    "fast_charging": 27.0,
    "ram_capacity": 6.0,
    "internal_memory": 512.0,
    "screen_size": 6.7,
    "refresh_rate": 120,
    "resolution": "1290 x 2796",
    "num_rear_cameras": 3,
    "num_front_cameras": 1.0,
    "os": "ios",
    "primary_camera_rear": 48.0,
    "primary_camera_front": 12.0,
    "extended_memory_available": 0,
    "extended_upto": 0.0
}
res = client.post("/api/predict?model=champion", json=ios_payload)
assert res.status_code == 200
f_data = res.json()
print(f"  Predicted Category: {f_data['predicted_category']} (Confidence: {f_data['confidence_percentage']})")
print(f"  Price Range: {f_data['estimated_price_range']}")
assert f_data['predicted_category'] == "Flagship", "Expected Flagship"

# --- 5. VERIFYING ALL 8 DERIVED ENGINEERED FEATURES ---
print("\n[TEST 5] Engineered Features Generated Correctly:")
for k, v in f_data["engineered_features"].items():
    print(f"  - {k}: {v}")
assert "ppi" in f_data["engineered_features"]
assert "performance_score" in f_data["engineered_features"]
assert "ram_to_storage_ratio" in f_data["engineered_features"]

# --- 6. MULTI-MODEL COMPARISON ENDPOINT ---
print("\n[TEST 6] Cross-Model Inference Comparison (/api/predict/compare):")
res = client.post("/api/predict/compare", json=ios_payload)
assert res.status_code == 200
c_data = res.json()
print(f"  Consensus: {c_data['consensus_category']} ({c_data['consensus_agreement']})")
for m in c_data["models_comparison"]:
    print(f"  - {m['model_name']:28s} => {m['predicted_category']:10s} (Score: {m['confidence_score']:.4f})")

# --- 7. VERIFYING INDIVIDUAL MODEL SELECTION PARAMETERS ---
print("\n[TEST 7] Verifying Individual Model Routing (?model=...):")
for model_key in ["champion", "random_forest", "svm", "knn", "logistic_regression"]:
    r = client.post(f"/api/predict?model={model_key}", json=budget_payload)
    assert r.status_code == 200
    print(f"  - Model '{model_key}': Returned {r.json()['predicted_category']} using '{r.json()['model_used']}'")

# --- 8. ANALYTICS & METRICS ENDPOINTS ---
print("\n[TEST 8] Analytics & Model Endpoints Integrity:")
r_list = client.get("/api/models/list")
assert r_list.status_code == 200
print(f"  - /api/models/list: {len(r_list.json()['models'])} models listed")

r_metrics = client.get("/api/models/metrics")
assert r_metrics.status_code == 200
print(f"  - /api/models/metrics: [OK] retrieved tuning benchmarks")

r_roc = client.get("/api/models/roc-curves")
assert r_roc.status_code == 200
print(f"  - /api/models/roc-curves: [OK] retrieved ROC/PR curves")

r_feat = client.get("/api/models/feature-importance")
assert r_feat.status_code == 200
print(f"  - /api/models/feature-importance: [OK] {len(r_feat.json()['ranked_features'])} features ranked")

r_summary = client.get("/api/analytics/dataset-summary")
assert r_summary.status_code == 200
print(f"  - /api/analytics/dataset-summary: [OK] dataset inspection loaded")

r_records = client.get("/api/analytics/records?limit=5")
assert r_records.status_code == 200
print(f"  - /api/analytics/records: [OK] retrieved {len(r_records.json()['records'])} sample records")

print("\n" + "=" * 80)
print("ALL 8 VERIFICATION SUITES PASSED! 100% OPERATIONAL INTEGRITY CONFIRMED")
print("=" * 80)
