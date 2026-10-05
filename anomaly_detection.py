import pandas as pd
from sklearn.ensemble import IsolationForest

# ==================================================
# 1. LOAD INDUSTRIAL DATA
# ==================================================

data = pd.read_csv("data/industrial_dataset.csv")

print("========== SMART INDUSTRY AI ==========")
print()
print("Industrial dataset loaded successfully!")

# ==================================================
# 2. SELECT SENSOR FEATURES
# ==================================================

features = [
    "temperature",
    "vibration",
    "current",
    "rpm",
    "pressure",
    "energy_consumption",
    "operating_hours"
]

X = data[features]

# ==================================================
# 3. CREATE ANOMALY DETECTION MODEL
# ==================================================

print()
print("========== TRAINING ANOMALY DETECTOR ==========")

anomaly_model = IsolationForest(
    contamination=0.05,
    random_state=42
)

anomaly_model.fit(X)

print("Anomaly detection model trained!")

# ==================================================
# 4. DETECT ANOMALIES
# ==================================================

data["anomaly"] = anomaly_model.predict(X)

# Isolation Forest:
#  1  = Normal
# -1  = Anomaly

data["anomaly_status"] = data["anomaly"].map({
    1: "NORMAL",
    -1: "ANOMALY"
})

# ==================================================
# 5. DISPLAY OVERALL RESULTS
# ==================================================

print()
print("========== ANOMALY RESULTS ==========")

print(
    data["anomaly_status"].value_counts()
)

# ==================================================
# 6. MACHINE-WISE ANOMALIES
# ==================================================

print()
print("========== MACHINE-WISE ANOMALIES ==========")

machine_anomalies = (
    data[data["anomaly"] == -1]
    .groupby("machine_id")
    .size()
)

print(machine_anomalies)

# ==================================================
# 7. TEST A NEW MACHINE READING
# ==================================================

print()
print("========== TEST MACHINE ==========")

test_machine = pd.DataFrame([{
    "temperature": 56.0,
    "vibration": 5.2,
    "current": 11.5,
    "rpm": 1200,
    "pressure": 4.5,
    "energy_consumption": 16.0,
    "operating_hours": 3000
}])

test_result = anomaly_model.predict(test_machine)[0]

if test_result == -1:
    print("🚨 ANOMALY DETECTED")
else:
    print("✅ MACHINE BEHAVIOR NORMAL")

# ==================================================
# 8. COMPLETE
# ==================================================

print()
print("========== ANOMALY ANALYSIS COMPLETE ==========")