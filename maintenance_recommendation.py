import pandas as pd
import joblib

# ==============================================================================
# SMART INDUSTRY AI - INDUCTION MACHINE MAINTENANCE RECOMMENDER
# ==============================================================================
# Prescriptive engineering recommendations for 3-Phase Induction Motors 
# addressing Stator, Rotor, Bearings, Thermal Overload, and Power Quality.
# ==============================================================================

try:
    failure_model = joblib.load("models/failure_prediction_model.pkl")
    component_model = joblib.load("models/component_fault_model.pkl")
except Exception as e:
    print(f"Error loading models: {e}")
    exit(1)

# Diagnostic Recommendation Knowledge Base
RECOMMENDATIONS_MAP = {
    "Normal": {
        "priority": "P4 - Routine",
        "action": "Continue normal automated telemetry monitoring.",
        "steps": [
            "Maintain standard periodic lubrication schedules.",
            "Log monthly baseline vibration and thermal scans.",
            "Verify cooling airflow pathways remain clean."
        ],
        "turnaround_time": "Standard scheduled inspection"
    },
    "Stator Winding Inter-Turn Fault": {
        "priority": "P1 - Critical",
        "action": "Immediate stator insulation diagnostic & mitigation.",
        "steps": [
            "De-energize motor and perform Lockout/Tagout (LOTO).",
            "Conduct DC winding resistance measurement (check phase balance < 2%).",
            "Perform Megohmmeter (Megger 1000V DC) insulation test and Surge Comparison test.",
            "Inspect stator end-turns for localized scorching or insulation carbonization.",
            "Schedule VPI (Vacuum Pressure Impregnation) re-varnish or full stator rewind."
        ],
        "turnaround_time": "Within 4 to 12 Hours"
    },
    "Broken Rotor Bars": {
        "priority": "P2 - High",
        "action": "Rotor bar / end-ring integrity assessment.",
        "steps": [
            "Execute High-Resolution Motor Current Signature Analysis (MCSA) around fundamental 50Hz sidebands (1±2s)fs.",
            "Perform single-phase low-voltage rotor rotation test to detect torque dips.",
            "Inspect squirrel-cage end-ring braze joints for thermal cracking.",
            "Plan rotor replacement or induction brazing repair."
        ],
        "turnaround_time": "Within 24 to 48 Hours"
    },
    "Bearing Degradation": {
        "priority": "P1 - Critical",
        "action": "Drive-End / Non-Drive-End bearing inspection and replacement.",
        "steps": [
            "Measure high-frequency shock pulse / crest factor on DE and NDE bearing housings.",
            "Check for lubricant starvation, contamination, or grease breakdown.",
            "Purge old grease and inject manufacturer-specified Polyurea/Lithium EP2 grease.",
            "If vibration velocity > 4.5 mm/s persists, replace bearing set (e.g. SKF 6309 C3) and check shaft journal fit."
        ],
        "turnaround_time": "Within 8 to 24 Hours"
    },
    "Rotor Eccentricity & Misalignment": {
        "priority": "P2 - High",
        "action": "Laser alignment, soft-foot correction, and air-gap verification.",
        "steps": [
            "Perform 4-point feeler gauge air-gap measurement around stator-rotor bore (ensure deviation < 10%).",
            "Check motor feet for soft-foot condition (< 0.05 mm tolerance).",
            "Perform precision dual-laser shaft alignment with driven equipment (angular & parallel offset < 0.05 mm).",
            "Inspect flexible coupling elements for elastomer wear or backlash."
        ],
        "turnaround_time": "Within 24 to 48 Hours"
    },
    "Thermal Overload & Cooling Blockage": {
        "priority": "P2 - High",
        "action": "Thermal airflow restoration and load derating check.",
        "steps": [
            "Clear debris and dust accumulation from external cooling fins and fan cowl.",
            "Inspect external cooling fan for broken or deformed blades.",
            "Verify driven equipment load torque does not exceed motor nameplate service factor (SF 1.15).",
            "Verify ambient temperature does not exceed motor rating (40°C Class B/F)."
        ],
        "turnaround_time": "Within 12 Hours"
    },
    "Phase Imbalance & Supply Distortion": {
        "priority": "P1 - Critical",
        "action": "Power quality analysis and supply contactor inspection.",
        "steps": [
            "Measure line-to-line voltages (ensure voltage unbalance < 1% per NEMA MG-1).",
            "Inspect main contactor and circuit breaker contacts for pitting or loose terminal lugs.",
            "Check power factor correction capacitor banks and harmonic filters.",
            "Examine VFD inverter switching pulses if fed through a frequency converter."
        ],
        "turnaround_time": "Within 4 to 8 Hours"
    }
}

# Example reading
test_reading = pd.DataFrame([{
    "temperature": 86.0,
    "vibration": 5.4,
    "current": 36.5,
    "rpm": 1420.0,
    "pressure": 3.2,
    "energy_consumption": 22.0,
    "operating_hours": 3200.0
}])

fault_prediction = component_model.predict(test_reading)[0]
prob = max(component_model.predict_proba(test_reading)[0]) * 100.0
rec = RECOMMENDATIONS_MAP.get(fault_prediction, RECOMMENDATIONS_MAP["Normal"])

print()
print("==========================================================")
print("  INDUCTION MACHINE PRESCRIPTIVE MAINTENANCE WORK ORDER")
print("==========================================================")
print(f"Detected Fault Diagnosis : {fault_prediction} (Confidence: {prob:.1f}%)")
print(f"Maintenance Priority    : {rec['priority']}")
print(f"Action Objective        : {rec['action']}")
print(f"Target Resolution Window: {rec['turnaround_time']}")
print("\nPrescriptive Standard Operating Procedures (SOP):")
for idx, step in enumerate(rec["steps"], 1):
    print(f"  {idx}. {step}")
print("==========================================================")