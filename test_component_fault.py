import pandas as pd
import joblib

# ==============================================================================
# SMART INDUSTRY AI - INDUCTION COMPONENT FAULT AI TEST
# ==============================================================================

print("==================================================")
print("SMART INDUSTRY AI - INDUCTION COMPONENT FAULT AI")
print("==================================================")

model = joblib.load("models/component_fault_model.pkl")

features = [
    "temperature",
    "vibration",
    "current",
    "rpm",
    "pressure",
    "energy_consumption",
    "operating_hours"
]

test_cases = {
    "1. NORMAL INDUCTION MOTOR": {
        "temperature": 58, "vibration": 1.4, "current": 24.0, "rpm": 1465, "pressure": 3.5, "energy_consumption": 14.2, "operating_hours": 1800
    },
    "2. BEARING RACE DEGRADATION": {
        "temperature": 74, "vibration": 6.2, "current": 27.0, "rpm": 1450, "pressure": 3.3, "energy_consumption": 16.8, "operating_hours": 3600
    },
    "3. STATOR WINDING INTER-TURN FAULT": {
        "temperature": 92, "vibration": 2.6, "current": 34.0, "rpm": 1435, "pressure": 3.2, "energy_consumption": 20.5, "operating_hours": 2800
    },
    "4. BROKEN ROTOR BARS (BRB)": {
        "temperature": 76, "vibration": 3.8, "current": 29.0, "rpm": 1390, "pressure": 3.3, "energy_consumption": 17.8, "operating_hours": 3200
    },
    "5. ROTOR ECCENTRICITY & MISALIGNMENT": {
        "temperature": 72, "vibration": 5.8, "current": 28.0, "rpm": 1420, "pressure": 3.1, "energy_consumption": 18.2, "operating_hours": 3100
    },
    "6. THERMAL OVERLOAD & COOLING BLOCKAGE": {
        "temperature": 104, "vibration": 3.1, "current": 39.0, "rpm": 1410, "pressure": 2.1, "energy_consumption": 24.5, "operating_hours": 2900
    },
    "7. PHASE UNBALANCE & SUPPLY DISTORTION": {
        "temperature": 88, "vibration": 4.2, "current": 36.0, "rpm": 1415, "pressure": 3.3, "energy_consumption": 22.8, "operating_hours": 2600
    }
}

for test_name, values in test_cases.items():
    input_data = pd.DataFrame([values], columns=features)
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    confidence = max(probabilities) * 100.0

    print()
    print("----------------------------------------------")
    print(test_name)
    print("----------------------------------------------")
    print("AI Fault Diagnosis:", prediction)
    print(f"Confidence        : {confidence:.2f}%")

print("\n==================================================")
print("INDUCTION FAULT TEST COMPLETED")
print("==================================================")