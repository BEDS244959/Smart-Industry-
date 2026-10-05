import pandas as pd
import joblib

# ==============================================================================
# SMART INDUSTRY AI - INDUCTION MOTOR AI EXPLAINABILITY & DIAGNOSTICS
# ==============================================================================
# Explains model predictions using Induction Motor feature attribution and 
# engineering physical threshold comparison.
# ==============================================================================

try:
    model = joblib.load("models/failure_prediction_model.pkl")
    print("========== SMART INDUSTRY AI ==========")
    print("Induction Motor AI Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Sample Induction Machine Telemetry (15kW Induction Motor under bearing stress)
machine_data = pd.DataFrame([{
    "temperature": 76.5,       # Stator winding temp (°C)
    "vibration": 4.85,         # DE Bearing vibration (mm/s RMS)
    "current": 32.5,           # Average Stator Current (A)
    "rpm": 1425.0,             # Rotor Speed (RPM)
    "pressure": 3.2,           # Coolant/Lube Pressure (bar)
    "energy_consumption": 18.2,# Active Power (kW)
    "operating_hours": 3650.0  # Operating Hours
}])

features = [
    "temperature",
    "vibration",
    "current",
    "rpm",
    "pressure",
    "energy_consumption",
    "operating_hours"
]

prediction = model.predict(machine_data[features])[0]
probabilities = model.predict_proba(machine_data[features])[0]
failure_probability = probabilities[1] * 100.0

print()
print("==========================================================")
print("       INDUCTION MOTOR PREDICTIVE DIAGNOSTICS")
print("==========================================================")
print(f"Failure Probability : {failure_probability:.2f}%")
print(f"AI Condition Status : {'[CRITICAL] FAILURE RISK DETECTED' if prediction == 1 else '[NORMAL] MACHINE OPERATING NORMALLY'}")
print("==========================================================")

# Feature Importance
importance = model.feature_importances_
feature_importance = pd.DataFrame({
    "feature": features,
    "importance": importance
}).sort_values(by="importance", ascending=False)

print("\n========== AI FEATURE ATTRIBUTION ==========")
for _, row in feature_importance.iterrows():
    print(f"  * {row['feature']:<20} -> {row['importance'] * 100:>6.2f} % weight")

print("\n========== INDUCTION MOTOR HEALTH ANALYSIS ==========")
temp_val = machine_data["temperature"].iloc[0]
vib_val = machine_data["vibration"].iloc[0]
curr_val = machine_data["current"].iloc[0]
rpm_val = machine_data["rpm"].iloc[0]

if temp_val > 75.0:
    print(f"[WARNING] Stator temperature ({temp_val:.1f} deg C) exceeds nominal baseline (warning > 75 C, critical > 88 C).")
if vib_val > 2.8:
    print(f"[WARNING] DE Bearing vibration ({vib_val:.2f} mm/s) exceeds ISO 10816-3 Zone B limit (2.8 mm/s).")
if rpm_val < 1430.0:
    print(f"[WARNING] Motor speed ({rpm_val:.0f} RPM) exhibits higher slip than nominal rated 1460 RPM.")
if curr_val > 30.0:
    print(f"[WARNING] Stator current draw ({curr_val:.1f} A) indicates elevated electrical/mechanical loading.")

print("\n==========================================================")
print("                 EXPLANATION COMPLETE")
print("==========================================================")