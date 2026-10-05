# Smart Industry AI — 3-Phase Induction Machine Digital Twin & Predictive Maintenance

## ⚡ Intelligent Induction Motor Telemetry, MCSA & Prescriptive Maintenance System

Smart Industry AI is an industrial-grade predictive maintenance and digital twin suite tailored for **Three-Phase Squirrel-Cage Induction Motors (SCIM)** based on **IEEE 841**, **NEMA MG-1**, **IEC 60034-30-1**, and **ISO 10816-3** standards.

It combines multi-physics telemetry generation, machine learning failure risk assessment, Motor Current Signature Analysis (MCSA), unsupervised anomaly detection, 7-class component fault diagnosis, interactive digital twin visualization, what-if sandbox simulation, and automated Twilio alert dispatch.

---

## 1. ⚙️ Induction Motor Fleet Specifications

| Motor ID | Machine Name | Application | Rated Power | Poles | Sync RPM | Rated Current | Base Load |
|---|---|---|---|---|---|---|---|
| **IM-101** | Centrifugal Slurry Pump Drive | Slurry Transfer | 15.0 kW (20 HP) | 4 | 1500 RPM | 29.5 A | 82% |
| **IM-102** | Cooling Tower Induced Draft Fan | Process Cooling | 11.0 kW (15 HP) | 4 | 1500 RPM | 22.0 A | 75% |
| **IM-103** | Rotary Screw Air Compressor | Plant Pneumatics | 22.0 kW (30 HP) | 2 | 3000 RPM | 41.5 A | 88% |
| **IM-104** | Heavy-Duty Material Conveyor | Bulk Material Handling | 7.5 kW (10 HP) | 4 | 1500 RPM | 15.2 A | 70% |
| **IM-105** | High-Torque Polymer Extruder | Polymer Manufacturing | 37.0 kW (50 HP) | 4 | 1500 RPM | 68.0 A | 90% |
| **IM-106** | HVAC Chiller Water Pump | Facility Chilling | 18.5 kW (25 HP) | 4 | 1500 RPM | 35.0 A | 78% |
| **IM-107** | High-Pressure Boiler Feed Pump | Steam Generation | 45.0 kW (60 HP) | 2 | 3000 RPM | 82.0 A | 85% |

---

## 2. 🔬 Induction Machine Physics & Diagnostic Parameters

The system models and processes comprehensive physical telemetry:
- **Electrical Dynamics**: 3-Phase RMS Stator Currents ($I_R, I_Y, I_B$), Current Unbalance (%), Line Voltage ($V_{rms}$), Operating Power Factor ($\cos\phi$), Active Power ($P$, kW), Reactive Power ($Q$, kVAR), Electrical Efficiency ($\eta$, %).
- **Mechanical & Kinematics**: Operating Rotor Speed ($N$, RPM), Synchronous Speed ($N_s$, RPM), Slip ($s = \frac{N_s - N}{N_s} \times 100\%$), Mechanical Load (%).
- **Vibration & Acoustics (ISO 10816-3)**: Drive-End (DE) Radial Vibration, Non-Drive-End (NDE) Radial Vibration, Axial Vibration, Vibration Crest Factor, Acoustic Noise (dBA).
- **Thermal RTD Pt100 Telemetry**: Stator Winding Temperature (°C) [Class F Limit 105°C rise], DE Bearing Temperature (°C), NDE Bearing Temperature (°C), Cooling Differential Pressure (bar).

---

## 3. 🧠 7-Class AI Component Fault Localization

The multi-class Random Forest diagnostic model detects:
1. **Normal Operation (Baseline)**: Optimal currents, low slip (<2.5%), ISO Zone A vibration (<1.4 mm/s), normal winding temp (55-65°C).
2. **Stator Winding Inter-Turn Fault**: High phase current unbalance (>15%), localized stator hot spots (>90°C), elevated THD.
3. **Broken Rotor Bars (BRB)**: Characteristic current sidebands at $(1 \pm 2s)f_s$, rotational speed pulsations, slip fluctuation (>6%).
4. **Bearing Degradation (DE/NDE)**: High high-frequency crest factor (>4.5), vibration velocity >4.5 mm/s (ISO Zone D), localized bearing heating.
5. **Rotor Dynamic Eccentricity & Misalignment**: 1X/2X rotational frequency vibration, air-gap flux unbalance, elevated axial vibration.
6. **Thermal Overload & Cooling Blockage**: High thermal stress (>100°C), low cooling differential pressure, prolonged full-load operation.
7. **Phase Imbalance & Supply Distortion**: Grid voltage distortion, heavy negative sequence current, severe motor torque ripple.

---

## 4. 🚀 Quick Start Guide

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate Induction Motor Telemetry & Train AI Models
```bash
# 1. Generate Physics-informed Induction Machine Datasets
python generate_data.py
python generate_component_fault_data.py

# 2. Train AI Failure, Multi-Class Fault & Anomaly Detection Models
python train_model.py
python train_component_fault_model.py
python train_anomaly_model.py
```

### Step 3: Launch the Streamlit Digital Twin Dashboard
```bash
streamlit run app.py
```

---

## 5. 🖥️ Dashboard Feature Overview

- **🏭 Fleet Overview**: Real-time KPI matrix, digital asset status cards, fleet health index (MHI) ranking, plant-wide active power demand.
- **📡 Live Digital Twin**: Real-time cross-section subsystem map (Stator, Rotor, DE Bearing, NDE Bearing, Terminal Box), ISO 10816 vibration gauge, live 3-phase current waveform oscilloscope, MCSA frequency spectrum visualizer.
- **🧠 AI Diagnostics & SOP**: Multi-class diagnostic confidence, ISO severity rating, SHAP-style feature attribution, and prescriptive engineering SOP work orders.
- **📈 Sandbox & What-If**: Interactive parameter sliders to test physical induction motor conditions in real-time.
- **🚨 Alerts & Gateway**: Active work order tracking, historical anomaly logs, manual & automated SMS dispatch console via Twilio.
- **📊 Model Governance**: Confusion matrix heatmaps, ROC-AUC, classification reports, and decision threshold calibration sliders.
