import pandas as pd
import joblib

# ==================================================
# 1. LOAD TRAINED AI MODEL
# ==================================================

model = joblib.load("models/failure_prediction_model.pkl")

print("========== SMART INDUSTRY AI ==========")
print()
print("AI model loaded successfully!")

# ==================================================
# 2. MACHINE SENSOR DATA
# ==================================================

machine_data = pd.DataFrame([{
    "temperature": 56.0,
    "vibration": 5.2,
    "current": 11.5,
    "rpm": 1200,
    "pressure": 4.5,
    "energy_consumption": 16.0,
    "operating_hours": 3000
}])

print()
print("========== MACHINE SENSOR DATA ==========")

print(machine_data)

# ==================================================
# 3. AI PREDICTION
# ==================================================

prediction = model.predict(machine_data)[0]

probability = model.predict_proba(machine_data)[0]

failure_probability = probability[1] * 100

# ==================================================
# 4. DISPLAY RESULT
# ==================================================

print()
print("========== AI PREDICTION ==========")

if prediction == 1:
    print("🚨 FAILURE RISK DETECTED")
else:
    print("✅ MACHINE CONDITION NORMAL")

print(
    "Failure probability:",
    round(failure_probability, 2),
    "%"
)

# ==================================================
# 5. RECOMMENDATION
# ==================================================

print()
print("========== RECOMMENDATION ==========")

if prediction == 1:
    print("⚠️ Schedule maintenance for this machine.")
else:
    print("✅ Continue normal machine operation.")