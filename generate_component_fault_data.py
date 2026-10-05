import numpy as np
import pandas as pd

# ==============================================================================
# SMART INDUSTRY AI - INDUCTION MACHINE COMPONENT FAULT GENERATOR
# ==============================================================================
# Generates balanced multi-class diagnostic telemetry for specific 3-Phase 
# Induction Motor faults according to electrical machine diagnostic theory.
# ==============================================================================

np.random.seed(42)
SAMPLES_PER_CLASS = 700
records = []

def add_fault_class_samples(
    fault_name,
    temp_range,
    stator_temp_range,
    de_bearing_temp_range,
    vib_range,
    vib_nde_range,
    axial_vib_range,
    crest_factor_range,
    current_range,
    unbalance_range,
    rpm_range,
    slip_range,
    pf_range,
    pressure_range,
    energy_range,
    thd_range,
    noise_range,
    hours_range
):
    for _ in range(SAMPLES_PER_CLASS):
        temp = np.random.normal(temp_range[0], temp_range[1])
        stator_t = np.random.normal(stator_temp_range[0], stator_temp_range[1])
        de_bearing_t = np.random.normal(de_bearing_temp_range[0], de_bearing_temp_range[1])
        vib = np.random.normal(vib_range[0], vib_range[1])
        vib_nde = np.random.normal(vib_nde_range[0], vib_nde_range[1])
        axial_vib = np.random.normal(axial_vib_range[0], axial_vib_range[1])
        crest = np.random.normal(crest_factor_range[0], crest_factor_range[1])
        curr = np.random.normal(current_range[0], current_range[1])
        unbalance = np.random.normal(unbalance_range[0], unbalance_range[1])
        r = np.random.normal(rpm_range[0], rpm_range[1])
        s = np.random.normal(slip_range[0], slip_range[1])
        pf = np.random.normal(pf_range[0], pf_range[1])
        press = np.random.normal(pressure_range[0], pressure_range[1])
        nrg = np.random.normal(energy_range[0], energy_range[1])
        thd = np.random.normal(thd_range[0], thd_range[1])
        noise = np.random.normal(noise_range[0], noise_range[1])
        hrs = np.random.normal(hours_range[0], hours_range[1])

        records.append({
            "temperature": round(float(np.clip(temp, 20.0, 130.0)), 2),
            "stator_temp": round(float(np.clip(stator_t, 25.0, 140.0)), 2),
            "de_bearing_temp": round(float(np.clip(de_bearing_t, 25.0, 120.0)), 2),
            "vibration": round(float(np.clip(vib, 0.4, 15.0)), 3),
            "vibration_de_radial": round(float(np.clip(vib, 0.4, 15.0)), 3),
            "vibration_nde_radial": round(float(np.clip(vib_nde, 0.3, 12.0)), 3),
            "vibration_axial": round(float(np.clip(axial_vib, 0.2, 10.0)), 3),
            "crest_factor": round(float(np.clip(crest, 1.4, 8.5)), 2),
            "current": round(float(np.clip(curr, 2.0, 85.0)), 2),
            "current_unbalance_pct": round(float(np.clip(unbalance, 0.2, 45.0)), 2),
            "rpm": round(float(np.clip(r, 600.0, 3100.0)), 1),
            "slip_pct": round(float(np.clip(s, 0.5, 25.0)), 2),
            "power_factor": round(float(np.clip(pf, 0.35, 0.95)), 3),
            "pressure": round(float(np.clip(press, 1.0, 6.0)), 2),
            "energy_consumption": round(float(np.clip(nrg, 2.0, 90.0)), 2),
            "thd_pct": round(float(np.clip(thd, 1.0, 35.0)), 2),
            "noise_dba": round(float(np.clip(noise, 55.0, 110.0)), 1),
            "operating_hours": round(float(np.clip(hrs, 200.0, 8000.0)), 1),
            "fault_type": fault_name
        })

# 1. NORMAL OPERATION
add_fault_class_samples(
    "Normal",
    temp_range=(58, 4),
    stator_temp_range=(60, 4),
    de_bearing_temp_range=(50, 3.5),
    vib_range=(1.4, 0.25),
    vib_nde_range=(1.2, 0.2),
    axial_vib_range=(0.8, 0.15),
    crest_factor_range=(2.2, 0.2),
    current_range=(24, 2.0),
    unbalance_range=(1.2, 0.4),
    rpm_range=(1465, 12),
    slip_range=(2.3, 0.4),
    pf_range=(0.86, 0.02),
    pressure_range=(3.5, 0.2),
    energy_range=(14.2, 1.2),
    thd_range=(2.5, 0.5),
    noise_range=(70, 2.5),
    hours_range=(1800, 350)
)

# 2. STATOR WINDING INTER-TURN FAULT
add_fault_class_samples(
    "Stator Winding Inter-Turn Fault",
    temp_range=(92, 6.5),
    stator_temp_range=(98, 7.0),
    de_bearing_temp_range=(64, 4.0),
    vib_range=(2.6, 0.45),
    vib_nde_range=(2.2, 0.35),
    axial_vib_range=(1.4, 0.25),
    crest_factor_range=(2.6, 0.3),
    current_range=(34, 3.5),
    unbalance_range=(16.5, 2.8),
    rpm_range=(1435, 20),
    slip_range=(4.3, 0.7),
    pf_range=(0.74, 0.03),
    pressure_range=(3.2, 0.3),
    energy_range=(20.5, 2.0),
    thd_range=(14.2, 2.1),
    noise_range=(82, 3.0),
    hours_range=(2800, 500)
)

# 3. BROKEN ROTOR BARS (BRB)
add_fault_class_samples(
    "Broken Rotor Bars",
    temp_range=(76, 5.0),
    stator_temp_range=(78, 5.5),
    de_bearing_temp_range=(62, 4.0),
    vib_range=(3.8, 0.55),
    vib_nde_range=(3.4, 0.45),
    axial_vib_range=(3.6, 0.5),
    crest_factor_range=(3.4, 0.4),
    current_range=(29, 3.0),
    unbalance_range=(6.2, 1.2),
    rpm_range=(1390, 35),
    slip_range=(7.3, 1.4),
    pf_range=(0.78, 0.03),
    pressure_range=(3.3, 0.25),
    energy_range=(17.8, 1.8),
    thd_range=(8.8, 1.5),
    noise_range=(84, 3.5),
    hours_range=(3200, 600)
)

# 4. BEARING DEGRADATION (DE / NDE RACE DEFECT)
add_fault_class_samples(
    "Bearing Degradation",
    temp_range=(74, 4.5),
    stator_temp_range=(72, 4.5),
    de_bearing_temp_range=(88, 6.0),
    vib_range=(6.2, 0.85),
    vib_nde_range=(4.8, 0.65),
    axial_vib_range=(2.2, 0.35),
    crest_factor_range=(5.6, 0.75),
    current_range=(27, 2.5),
    unbalance_range=(2.4, 0.6),
    rpm_range=(1450, 18),
    slip_range=(3.3, 0.6),
    pf_range=(0.82, 0.025),
    pressure_range=(3.3, 0.25),
    energy_range=(16.8, 1.5),
    thd_range=(4.5, 0.8),
    noise_range=(89, 4.0),
    hours_range=(3600, 700)
)

# 5. ROTOR ECCENTRICITY & MISALIGNMENT
add_fault_class_samples(
    "Rotor Eccentricity & Misalignment",
    temp_range=(72, 4.5),
    stator_temp_range=(74, 4.5),
    de_bearing_temp_range=(76, 5.0),
    vib_range=(5.8, 0.75),
    vib_nde_range=(5.4, 0.70),
    axial_vib_range=(4.9, 0.65),
    crest_factor_range=(3.2, 0.35),
    current_range=(28, 2.8),
    unbalance_range=(5.5, 1.1),
    rpm_range=(1420, 25),
    slip_range=(5.3, 0.9),
    pf_range=(0.80, 0.03),
    pressure_range=(3.1, 0.3),
    energy_range=(18.2, 1.6),
    thd_range=(6.8, 1.2),
    noise_range=(86, 3.2),
    hours_range=(3100, 550)
)

# 6. THERMAL OVERLOAD & COOLING BLOCKAGE
add_fault_class_samples(
    "Thermal Overload & Cooling Blockage",
    temp_range=(104, 7.0),
    stator_temp_range=(108, 7.5),
    de_bearing_temp_range=(84, 5.5),
    vib_range=(3.1, 0.4),
    vib_nde_range=(2.7, 0.35),
    axial_vib_range=(1.5, 0.25),
    crest_factor_range=(2.5, 0.25),
    current_range=(39, 3.8),
    unbalance_range=(2.8, 0.7),
    rpm_range=(1410, 22),
    slip_range=(6.0, 0.8),
    pf_range=(0.87, 0.02),
    pressure_range=(2.1, 0.25),
    energy_range=(24.5, 2.5),
    thd_range=(5.2, 0.9),
    noise_range=(81, 3.0),
    hours_range=(2900, 600)
)

# 7. PHASE IMBALANCE & SUPPLY DISTORTION
add_fault_class_samples(
    "Phase Imbalance & Supply Distortion",
    temp_range=(88, 5.5),
    stator_temp_range=(92, 6.0),
    de_bearing_temp_range=(68, 4.5),
    vib_range=(4.2, 0.6),
    vib_nde_range=(3.8, 0.5),
    axial_vib_range=(2.8, 0.4),
    crest_factor_range=(3.0, 0.35),
    current_range=(36, 4.0),
    unbalance_range=(22.5, 3.5),
    rpm_range=(1415, 28),
    slip_range=(5.6, 1.0),
    pf_range=(0.68, 0.04),
    pressure_range=(3.3, 0.25),
    energy_range=(22.8, 2.2),
    thd_range=(18.5, 2.5),
    noise_range=(87, 3.5),
    hours_range=(2600, 500)
)

df = pd.DataFrame(records)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("data/component_fault_dataset.csv", index=False)

print("==========================================================")
print("SMART INDUSTRY AI - INDUCTION COMPONENT FAULT DATASET")
print("==========================================================")
print(f"Total Samples Generated: {len(df)}")
print("Class Distribution:")
print(df["fault_type"].value_counts())
print("Saved to data/component_fault_dataset.csv successfully!")
print("==========================================================")