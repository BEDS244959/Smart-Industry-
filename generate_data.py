import pandas as pd
import numpy as np

# ==============================================================================
# SMART INDUSTRY AI - INDUCTION MACHINE TELEMETRY GENERATOR
# ==============================================================================
# Physics-informed synthetic data generator for Three-Phase Squirrel Cage 
# Induction Motors (SCIM) based on IEEE 841, NEMA MG-1, and ISO 10816-3 standards.
# ==============================================================================

np.random.seed(42)

# ------------------------------------------------------------------------------
# INDUCTION MACHINE FLEET CONFIGURATION
# ------------------------------------------------------------------------------
INDUCTION_MACHINES = {
    "IM-101": {
        "name": "Centrifugal Slurry Pump Drive",
        "rated_power_kw": 15.0,
        "poles": 4,
        "rated_rpm": 1460,
        "rated_current": 29.5,
        "base_load": 0.82,
        "nominal_temp": 62.0,
        "nominal_vib": 1.35,
        "bias": 0.01
    },
    "IM-102": {
        "name": "Cooling Tower Induced Draft Fan",
        "rated_power_kw": 11.0,
        "poles": 4,
        "rated_rpm": 1455,
        "rated_current": 22.0,
        "base_load": 0.75,
        "nominal_temp": 58.0,
        "nominal_vib": 1.50,
        "bias": 0.02
    },
    "IM-103": {
        "name": "Rotary Screw Air Compressor",
        "rated_power_kw": 22.0,
        "poles": 2,
        "rated_rpm": 2940,
        "rated_current": 41.5,
        "base_load": 0.88,
        "nominal_temp": 68.0,
        "nominal_vib": 1.80,
        "bias": 0.04
    },
    "IM-104": {
        "name": "Heavy-Duty Raw Material Conveyor",
        "rated_power_kw": 7.5,
        "poles": 4,
        "rated_rpm": 1440,
        "rated_current": 15.2,
        "base_load": 0.70,
        "nominal_temp": 54.0,
        "nominal_vib": 1.20,
        "bias": 0.01
    },
    "IM-105": {
        "name": "High-Torque Polymer Extruder",
        "rated_power_kw": 37.0,
        "poles": 4,
        "rated_rpm": 1475,
        "rated_current": 68.0,
        "base_load": 0.90,
        "nominal_temp": 72.0,
        "nominal_vib": 1.65,
        "bias": 0.05
    },
    "IM-106": {
        "name": "HVAC Chiller Water Pump",
        "rated_power_kw": 18.5,
        "poles": 4,
        "rated_rpm": 1465,
        "rated_current": 35.0,
        "base_load": 0.78,
        "nominal_temp": 60.0,
        "nominal_vib": 1.40,
        "bias": 0.02
    },
    "IM-107": {
        "name": "High-Pressure Boiler Feed Pump",
        "rated_power_kw": 45.0,
        "poles": 2,
        "rated_rpm": 2960,
        "rated_current": 82.0,
        "base_load": 0.85,
        "nominal_temp": 70.0,
        "nominal_vib": 1.95,
        "bias": 0.06
    }
}

GRID_FREQUENCY = 50.0  # Hz (Nominal European / Asian grid)
NOMINAL_VOLTAGE = 400.0 # V Line-to-Line RMS

records = []

for machine_id, spec in INDUCTION_MACHINES.items():
    sync_rpm = (120.0 * GRID_FREQUENCY) / spec["poles"]
    rated_kw = spec["rated_power_kw"]
    rated_current = spec["rated_current"]
    base_load = spec["base_load"]
    bias = spec["bias"]
    
    for reading_num in range(500):
        # ----------------------------------------------------------------------
        # PROGRESSIVE DEGRADATION / FAULT EVOLUTION
        # ----------------------------------------------------------------------
        # Most readings are healthy (~80%); some experience progressive wear (~14%) or critical fault (~6%)
        degradation_raw = np.random.beta(2.2, 5.0) + bias + np.random.normal(0, 0.035)
        degradation = float(np.clip(degradation_raw, 0.0, 1.0))
        
        # Load variation around base load
        load_pct = np.clip(np.random.normal(base_load, 0.08) + 0.15 * degradation, 0.25, 1.25)
        
        # Determine primary degradation mechanism if degrading
        fault_selector = np.random.choice([
            "Normal",
            "Stator Winding Inter-Turn Fault",
            "Broken Rotor Bars",
            "Bearing Degradation",
            "Rotor Eccentricity & Misalignment",
            "Thermal Overload & Cooling Blockage",
            "Phase Imbalance & Supply Distortion"
        ], p=[0.45, 0.11, 0.10, 0.13, 0.09, 0.06, 0.06] if degradation > 0.32 else [0.95, 0.01, 0.01, 0.015, 0.01, 0.0025, 0.0025])

        # ----------------------------------------------------------------------
        # INDUCTION MOTOR PHYSICS & SIGNATURES
        # ----------------------------------------------------------------------
        # Nominal slip increases with mechanical load and rotor bar degradation
        nominal_slip = ((sync_rpm - spec["rated_rpm"]) / sync_rpm) * load_pct
        if fault_selector == "Broken Rotor Bars":
            slip = nominal_slip * (1.0 + 1.6 * degradation) + np.random.normal(0, 0.004)
        else:
            slip = nominal_slip * (1.0 + 0.25 * degradation) + np.random.normal(0, 0.002)
        slip = float(np.clip(slip, 0.008, 0.14))
        
        rpm = sync_rpm * (1.0 - slip) + np.random.normal(0, 4.0)
        
        # Three Phase Currents & Unbalance
        base_current = rated_current * (0.32 + 0.68 * load_pct)
        ir = np.random.normal(base_current, 0.4)
        iy = np.random.normal(base_current, 0.4)
        ib = np.random.normal(base_current, 0.4)
        
        if fault_selector == "Stator Winding Inter-Turn Fault":
            ir += (5.0 + 18.0 * degradation)
            iy -= (1.5 + 4.0 * degradation)
        elif fault_selector == "Phase Imbalance & Supply Distortion":
            ir += (4.0 + 14.0 * degradation)
            ib -= (3.5 + 10.0 * degradation)
        elif fault_selector == "Thermal Overload & Cooling Blockage":
            ir += (2.5 + 8.0 * degradation)
            iy += (2.5 + 8.0 * degradation)
            ib += (2.5 + 8.0 * degradation)

        avg_current = (ir + iy + ib) / 3.0
        max_dev = max(abs(ir - avg_current), abs(iy - avg_current), abs(ib - avg_current))
        current_unbalance_pct = float(np.clip((max_dev / (avg_current + 1e-5)) * 100.0, 0.4, 38.0))
        
        # Power Factor & Electrical Power
        pf_nominal = 0.85 if load_pct > 0.7 else (0.65 + 0.25 * load_pct)
        power_factor = float(np.clip(pf_nominal - (0.12 * degradation if fault_selector != "Normal" else 0.0) + np.random.normal(0, 0.015), 0.45, 0.93))
        
        voltage_rms = float(np.random.normal(NOMINAL_VOLTAGE, 3.5) - (12.0 * degradation if fault_selector == "Phase Imbalance & Supply Distortion" else 0.0))
        active_power_kw = (np.sqrt(3.0) * voltage_rms * avg_current * power_factor) / 1000.0
        reactive_power_kvar = (np.sqrt(3.0) * voltage_rms * avg_current * np.sin(np.arccos(power_factor))) / 1000.0
        
        # Efficiency
        ideal_eff = 91.5 + 2.0 * (rated_kw / 45.0)
        efficiency_pct = float(np.clip(ideal_eff - 14.0 * degradation - (current_unbalance_pct * 0.45) + np.random.normal(0, 0.5), 65.0, 96.0))
        
        # Thermal: Stator Winding, DE Bearing, NDE Bearing Temperatures
        ambient_temp = 28.0 + np.random.normal(0, 2.0)
        thermal_rise = (spec["nominal_temp"] - 28.0) * (load_pct ** 1.6)
        
        stator_temp = ambient_temp + thermal_rise + (35.0 * degradation if fault_selector in ["Stator Winding Inter-Turn Fault", "Thermal Overload & Cooling Blockage", "Phase Imbalance & Supply Distortion"] else 12.0 * degradation) + np.random.normal(0, 1.8)
        
        de_bearing_temp = ambient_temp + 0.75 * thermal_rise + (28.0 * degradation if fault_selector == "Bearing Degradation" else 8.0 * degradation) + np.random.normal(0, 1.5)
        nde_bearing_temp = ambient_temp + 0.65 * thermal_rise + (22.0 * degradation if fault_selector == "Bearing Degradation" else 6.0 * degradation) + np.random.normal(0, 1.4)
        
        # Vibration Tri-Axial (ISO 10816-3 RMS mm/s) & Crest Factor
        vib_base = spec["nominal_vib"]
        if fault_selector == "Bearing Degradation":
            vibration_de = vib_base + 6.5 * degradation + np.random.normal(0, 0.4)
            vibration_nde = vib_base + 4.2 * degradation + np.random.normal(0, 0.3)
            crest_factor = 2.8 + 4.2 * degradation + np.random.normal(0, 0.3)
            axial_vib = 1.2 + 2.0 * degradation + np.random.normal(0, 0.2)
        elif fault_selector == "Rotor Eccentricity & Misalignment":
            vibration_de = vib_base + 5.0 * degradation + np.random.normal(0, 0.35)
            vibration_nde = vib_base + 4.8 * degradation + np.random.normal(0, 0.35)
            crest_factor = 2.2 + 1.2 * degradation + np.random.normal(0, 0.2)
            axial_vib = 1.5 + 4.5 * degradation + np.random.normal(0, 0.3)
        elif fault_selector == "Broken Rotor Bars":
            vibration_de = vib_base + 3.2 * degradation + np.random.normal(0, 0.3)
            vibration_nde = vib_base + 2.8 * degradation + np.random.normal(0, 0.25)
            crest_factor = 2.4 + 1.8 * degradation + np.random.normal(0, 0.2)
            axial_vib = 1.3 + 3.2 * degradation + np.random.normal(0, 0.25)
        else:
            vibration_de = vib_base + 1.2 * degradation + np.random.normal(0, 0.2)
            vibration_nde = vib_base + 1.0 * degradation + np.random.normal(0, 0.18)
            crest_factor = 2.1 + 0.6 * degradation + np.random.normal(0, 0.15)
            axial_vib = 0.9 + 0.8 * degradation + np.random.normal(0, 0.15)
            
        vibration_de = float(max(0.4, vibration_de))
        vibration_nde = float(max(0.3, vibration_nde))
        axial_vib = float(max(0.2, axial_vib))
        crest_factor = float(max(1.5, crest_factor))
        
        # Harmonic Distortion (THD %) & Noise (dBA)
        thd_pct = float(np.clip(2.2 + 8.5 * degradation + (current_unbalance_pct * 0.3) + np.random.normal(0, 0.4), 1.2, 28.0))
        noise_dba = float(np.clip(68.0 + 18.0 * degradation + (vibration_de * 2.2) + np.random.normal(0, 1.2), 62.0, 102.0))
        
        # Lubricant / Cooling Differential Pressure (bar)
        coolant_pressure = float(np.clip(3.6 - (1.2 * degradation if fault_selector == "Thermal Overload & Cooling Blockage" else 0.2 * degradation) + np.random.normal(0, 0.15), 1.5, 4.8))
        
        # Operating hours
        operating_hours = float(1200 + reading_num * 8 + np.random.normal(0, 45))
        
        # Backward compatibility summary features
        temperature = stator_temp
        vibration = vibration_de
        current = avg_current
        pressure = coolant_pressure
        energy_consumption = active_power_kw
        
        # Condition Score & ISO 10816 Severity
        is_critical_temp = (stator_temp >= 78.0) or (de_bearing_temp >= 74.0)
        is_critical_vib = (vibration_de >= 3.8) or (vibration_nde >= 3.4)
        is_critical_unbalance = (current_unbalance_pct >= 8.5)
        is_critical_slip = (slip >= 0.052)
        is_critical_crest = (crest_factor >= 3.8)
        is_critical_degradation = (degradation >= 0.52)
        
        condition_score = (
            0.35 * degradation
            + 0.16 * float(is_critical_temp)
            + 0.16 * float(is_critical_vib)
            + 0.11 * float(is_critical_unbalance)
            + 0.10 * float(is_critical_crest)
            + 0.07 * float(is_critical_slip)
            + 0.05 * float(operating_hours > 3600)
        )
        condition_score = float(np.clip(condition_score, 0.0, 1.0))
        
        failure = int(condition_score >= 0.42 or (degradation > 0.58) or (is_critical_temp and is_critical_vib))
        maintenance_required = int(condition_score >= 0.30 or failure == 1)
        
        if fault_selector == "Normal" and failure == 1:
            fault_selector = "Bearing Degradation"
        elif fault_selector == "Normal" and maintenance_required == 1:
            fault_selector = "Rotor Eccentricity & Misalignment"
            
        records.append({
            "machine_id": machine_id,
            "machine_name": spec["name"],
            "rated_power_kw": rated_kw,
            "temperature": round(temperature, 2),
            "vibration": round(vibration, 3),
            "current": round(current, 2),
            "rpm": round(rpm, 1),
            "pressure": round(pressure, 2),
            "energy_consumption": round(energy_consumption, 2),
            "operating_hours": round(operating_hours, 1),
            "stator_temp": round(stator_temp, 2),
            "de_bearing_temp": round(de_bearing_temp, 2),
            "nde_bearing_temp": round(nde_bearing_temp, 2),
            "current_r": round(ir, 2),
            "current_y": round(iy, 2),
            "current_b": round(ib, 2),
            "current_unbalance_pct": round(current_unbalance_pct, 2),
            "voltage_rms": round(voltage_rms, 1),
            "slip_pct": round(slip * 100.0, 2),
            "power_factor": round(power_factor, 3),
            "active_power_kw": round(active_power_kw, 2),
            "reactive_power_kvar": round(reactive_power_kvar, 2),
            "efficiency_pct": round(efficiency_pct, 2),
            "load_pct": round(load_pct * 100.0, 1),
            "vibration_de_radial": round(vibration_de, 3),
            "vibration_nde_radial": round(vibration_nde, 3),
            "vibration_axial": round(axial_vib, 3),
            "crest_factor": round(crest_factor, 2),
            "noise_dba": round(noise_dba, 1),
            "thd_pct": round(thd_pct, 2),
            "fault_type": fault_selector,
            "maintenance_required": maintenance_required,
            "failure": failure
        })

df = pd.DataFrame(records)
df.to_csv("data/industrial_dataset.csv", index=False)

print("==========================================================")
print("  SMART INDUSTRY AI - INDUCTION MACHINE DATASET GENERATOR")
print("==========================================================")
print(f"Total Readings Generated: {len(df)}")
print(f"Induction Machines: {df['machine_id'].nunique()}")
print(f"Failure Readings: {df['failure'].sum()} ({df['failure'].mean()*100:.2f}%)")
print(f"Maintenance Required: {df['maintenance_required'].sum()} ({df['maintenance_required'].mean()*100:.2f}%)")
print("\nFault Type Distribution:")
print(df["fault_type"].value_counts())
print("\nKey Induction Motor Baseline Averages:")
print(f"  • Avg Stator Temp: {df['stator_temp'].mean():.2f} °C")
print(f"  • Avg DE Vibration: {df['vibration_de_radial'].mean():.2f} mm/s RMS")
print(f"  • Avg Slip: {df['slip_pct'].mean():.2f} %")
print(f"  • Avg Current Unbalance: {df['current_unbalance_pct'].mean():.2f} %")
print(f"  • Avg Power Factor: {df['power_factor'].mean():.3f}")
print(f"  • Avg Efficiency: {df['efficiency_pct'].mean():.2f} %")
print("Saved to data/industrial_dataset.csv successfully!")
print("==========================================================")