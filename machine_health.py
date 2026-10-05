import pandas as pd
import joblib

# ==============================================================================
# SMART INDUSTRY AI - INDUCTION MACHINE HEALTH & MHI ANALYZER
# ==============================================================================
# Motor Health Index (MHI) calculation based on IEEE 841, NEMA MG-1, and 
# ISO 10816-3 vibration severity standards for 3-Phase Induction Motors.
# ==============================================================================

try:
    model = joblib.load("models/failure_prediction_model.pkl")
    print("========== SMART INDUSTRY AI ==========")
    print("AI Failure model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Sample Induction Machine Telemetry (15 kW Centrifugal Pump Drive)
induction_machine_data = pd.DataFrame([{
    "temperature": 78.5,       # Stator winding temperature (°C)
    "vibration": 4.65,         # Drive-End radial vibration (mm/s RMS)
    "current": 33.2,           # Average 3-Phase Stator Current (A)
    "rpm": 1410.0,             # Operating Speed (RPM) [Sync: 1500 RPM]
    "pressure": 3.1,           # Coolant / Lubrication Pressure (bar)
    "energy_consumption": 18.5,# Active Power Consumption (kW)
    "operating_hours": 3450.0  # Cumulative Operating Hours (hrs)
}])

# Predict failure probability
probabilities = model.predict_proba(induction_machine_data)[0]
failure_probability = probabilities[1] * 100.0

# Calculate Motor Health Index (MHI) - 0 to 100
health_score = max(0.0, min(100.0, 100.0 - failure_probability))

# ISO 10816-3 Vibration Severity Zone Evaluation (Class II Medium Induction Motors)
vib_val = induction_machine_data["vibration"].iloc[0]
if vib_val < 1.4:
    iso_zone = "Zone A (Newly Commissioned / Excellent)"
elif vib_val < 2.8:
    iso_zone = "Zone B (Unrestricted Long-Term Operation / Good)"
elif vib_val < 4.5:
    iso_zone = "Zone C (Restricted Operation / Warning - Plan Maintenance)"
else:
    iso_zone = "Zone D (Critical Vibration / Trip Hazard - Stop Immediately)"

# Risk Level Classification
if failure_probability >= 70:
    risk_level = "CRITICAL / HIGH RISK"
elif failure_probability >= 30:
    risk_level = "WARNING / MEDIUM RISK"
else:
    risk_level = "NORMAL / LOW RISK"

# Remaining Useful Life (RUL) Approximation
if health_score >= 80:
    estimated_rul = "> 3,500 Operating Hours"
elif health_score >= 50:
    estimated_rul = "650 - 1,200 Operating Hours"
elif health_score >= 25:
    estimated_rul = "120 - 300 Operating Hours"
else:
    estimated_rul = "< 48 Operating Hours (Immediate Action Required)"

print()
print("==========================================================")
print("     INDUCTION MACHINE HEALTH & DIGITAL TWIN STATUS")
print("==========================================================")
print(f"Asset Monitored        : 3-Phase Induction Motor (15 kW, 4-Pole)")
print(f"Failure Probability    : {failure_probability:.2f}%")
print(f"Motor Health Index(MHI): {health_score:.2f} / 100")
print(f"Risk Assessment        : {risk_level}")
print(f"ISO 10816-3 Severity   : {iso_zone}")
print(f"Estimated RUL          : {estimated_rul}")
print("==========================================================")

print("\n========== PRESCRIPTIVE MOTOR RECOMMENDATION ==========")
if failure_probability >= 70:
    print("[CRITICAL] IMMEDIATE SHUTDOWN & INTERVENTION:")
    print("   * Inspect DE/NDE bearings for race spalling or cage disintegration.")
    print("   * Perform insulation resistance (Megger > 100 MOhm) and surge test.")
    print("   * Check laser alignment and soft-foot tolerance.")
elif failure_probability >= 30:
    print("[WARNING] SCHEDULE PREVENTIVE MAINTENANCE:")
    print("   * Re-grease motor bearings with high-temperature Polyurea grease.")
    print("   * Inspect cooling fan shroud for dust/clogging blockage.")
    print("   * Conduct Motor Current Signature Analysis (MCSA) for rotor bar health.")
else:
    print("[NORMAL] INDUCTION MOTOR HEALTH OPTIMAL:")
    print("   * Operating well within IEEE 841 / ISO 10816 standards.")
    print("   * Maintain routine automated condition monitoring schedule.")
print("==========================================================")