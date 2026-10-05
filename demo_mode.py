import pandas as pd
import joblib

# ==============================================================================
# SMART INDUSTRY AI - INDUCTION MACHINE DEMO MODE SCENARIOS
# ==============================================================================

failure_model = joblib.load("models/failure_prediction_model.pkl")
anomaly_model = joblib.load("models/anomaly_detection_model.pkl")
component_model = joblib.load("models/component_fault_model.pkl")

features = [
    "temperature",
    "vibration",
    "current",
    "rpm",
    "pressure",
    "energy_consumption",
    "operating_hours"
]

scenarios = {
    "1. NORMAL INDUCTION MOTOR (Baseline)": {
        "temperature": 58.0,
        "vibration": 1.4,
        "current": 24.0,
        "rpm": 1465,
        "pressure": 3.5,
        "energy_consumption": 14.2,
        "operating_hours": 1800
    },
    "2. BEARING DEGRADATION (DE Race Defect)": {
        "temperature": 74.0,
        "vibration": 6.2,
        "current": 27.0,
        "rpm": 1450,
        "pressure": 3.3,
        "energy_consumption": 16.8,
        "operating_hours": 3600
    },
    "3. STATOR WINDING INTER-TURN FAULT": {
        "temperature": 92.0,
        "vibration": 2.6,
        "current": 34.0,
        "rpm": 1435,
        "pressure": 3.2,
        "energy_consumption": 20.5,
        "operating_hours": 2800
    },
    "4. BROKEN ROTOR BARS (BRB)": {
        "temperature": 76.0,
        "vibration": 3.8,
        "current": 29.0,
        "rpm": 1390,
        "pressure": 3.3,
        "energy_consumption": 17.8,
        "operating_hours": 3200
    },
    "5. ROTOR ECCENTRICITY & MISALIGNMENT": {
        "temperature": 72.0,
        "vibration": 5.8,
        "current": 28.0,
        "rpm": 1420,
        "pressure": 3.1,
        "energy_consumption": 18.2,
        "operating_hours": 3100
    },
    "6. THERMAL OVERLOAD & COOLING BLOCK": {
        "temperature": 104.0,
        "vibration": 3.1,
        "current": 39.0,
        "rpm": 1410,
        "pressure": 2.1,
        "energy_consumption": 24.5,
        "operating_hours": 2900
    },
    "7. PHASE UNBALANCE & SUPPLY DISTORTION": {
        "temperature": 88.0,
        "vibration": 4.2,
        "current": 36.0,
        "rpm": 1415,
        "pressure": 3.3,
        "energy_consumption": 22.8,
        "operating_hours": 2600
    }
}

print()
print("==========================================================")
print("     SMART INDUSTRY AI - INDUCTION MACHINE DEMO SUITE")
print("==========================================================")

for name, values in scenarios.items():
    df = pd.DataFrame([values])[features]
    fail_p = failure_model.predict_proba(df)[0][1] * 100.0
    anom_p = anomaly_model.predict(df)[0]
    fault_diag = component_model.predict(df)[0]
    conf = max(component_model.predict_proba(df)[0]) * 100.0
    
    health = max(0.0, min(100.0, 100.0 - fail_p))
    risk = "HIGH" if fail_p >= 70 else ("MEDIUM" if fail_p >= 30 else "LOW")
    anom_status = "ANOMALOUS" if anom_p == -1 else "NORMAL"
    
    print(f"\n----------------------------------------------------------")
    print(f"SCENARIO: {name}")
    print(f"----------------------------------------------------------")
    print(f"  Telemetry: Temp={values['temperature']}°C | Vib={values['vibration']}mm/s | Curr={values['current']}A | RPM={values['rpm']}")
    print(f"  AI Failure Risk     : {fail_p:.1f}% (Risk Level: {risk})")
    print(f"  Motor Health Index  : {health:.1f} / 100")
    print(f"  Anomaly Detection   : {anom_status}")
    print(f"  Fault Diagnosis AI  : {fault_diag} ({conf:.1f}% confidence)")

print("\n==========================================================")
print("                 DEMO SUITE COMPLETED")
print("==========================================================")