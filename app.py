import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Smart Industry AI — Induction Motor Digital Twin",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# PROFESSIONAL INDUSTRIAL SCADA STYLING
# ==============================================================================
st.markdown("""
<style>
    /* Industrial Dark Ergonomic Palette */
    :root {
        --bg-main: #0b1120;
        --bg-panel: #131d31;
        --bg-card: #1a263e;
        --border-subtle: #243552;
        --accent-cyan: #38bdf8;
        --accent-emerald: #10b981;
        --accent-amber: #f59e0b;
        --accent-rose: #f43f5e;
        --text-bright: #f8fafc;
        --text-muted: #94a3b8;
    }
    
    .stApp {
        background-color: var(--bg-main);
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Top SCADA Control Header */
    .scada-header {
        background: linear-gradient(90deg, #111e38 0%, #172a4d 50%, #111e38 100%);
        border: 1px solid #233a63;
        border-radius: 10px;
        padding: 16px 24px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }
    
    /* Technical Data Box */
    .telemetry-card {
        background: #152238;
        border: 1px solid #24395c;
        border-radius: 8px;
        padding: 14px 16px;
        text-align: center;
        transition: border-color 0.2s;
    }
    .telemetry-card:hover {
        border-color: var(--accent-cyan);
    }
    .telemetry-label {
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #8fa2be;
        margin-bottom: 4px;
        font-weight: 600;
    }
    .telemetry-value {
        font-size: 1.55rem;
        font-weight: 700;
        color: #ffffff;
        font-family: "SF Mono", Consolas, "Courier New", monospace;
        line-height: 1.2;
    }
    .telemetry-unit {
        font-size: 0.85rem;
        color: #8fa2be;
        font-weight: normal;
    }
    .telemetry-sub {
        font-size: 0.72rem;
        margin-top: 4px;
        color: #64748b;
    }
    
    /* Subsystem Status Block */
    .subsystem-card {
        background: #141f33;
        border: 1px solid #223450;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 10px;
    }
    
    /* Status Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .badge-ok {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .badge-warn {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .badge-crit {
        background: rgba(244, 63, 94, 0.15);
        color: #fb7185;
        border: 1px solid rgba(244, 63, 94, 0.35);
    }
    
    /* Custom Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid #233a63;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #121d30;
        border: 1px solid #233a63;
        border-radius: 6px 6px 0 0;
        color: #94a3b8;
        padding: 8px 18px;
        font-weight: 600;
        font-size: 0.90rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e2f4e !important;
        border-color: #38bdf8 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA & MODEL LOADING
# ==============================================================================
@st.cache_data
def load_dataset():
    return pd.read_csv("data/industrial_dataset.csv")

@st.cache_resource
def load_models():
    fail_mod = joblib.load("models/failure_prediction_model.pkl")
    thresh = float(joblib.load("models/failure_threshold.pkl")) if os.path.exists("models/failure_threshold.pkl") else 0.40
    anom_mod = joblib.load("models/anomaly_detection_model.pkl") if os.path.exists("models/anomaly_detection_model.pkl") else None
    comp_mod = joblib.load("models/component_fault_model.pkl") if os.path.exists("models/component_fault_model.pkl") else None
    return fail_mod, thresh, anom_mod, comp_mod

try:
    data = load_dataset()
    failure_model, failure_threshold, anomaly_model, component_fault_model = load_models()
except Exception as e:
    st.error(f"Error loading system assets: {e}")
    st.stop()

# ==============================================================================
# INDUCTION MOTOR SPECIFICATIONS CATALOG
# ==============================================================================
MOTOR_CATALOG = {
    "IM-101": {"name": "Centrifugal Slurry Pump", "kw": 15.0, "hp": 20.0, "poles": 4, "sync_rpm": 1500, "rated_rpm": 1460, "fla": 29.5, "app": "Slurry Transfer"},
    "IM-102": {"name": "Cooling Tower Fan", "kw": 11.0, "hp": 15.0, "poles": 4, "sync_rpm": 1500, "rated_rpm": 1455, "fla": 22.0, "app": "Process Cooling"},
    "IM-103": {"name": "Screw Air Compressor", "kw": 22.0, "hp": 30.0, "poles": 2, "sync_rpm": 3000, "rated_rpm": 2940, "fla": 41.5, "app": "Plant Pneumatics"},
    "IM-104": {"name": "Material Conveyor Drive", "kw": 7.5, "hp": 10.0, "poles": 4, "sync_rpm": 1500, "rated_rpm": 1440, "fla": 15.2, "app": "Bulk Handling"},
    "IM-105": {"name": "Polymer Extruder Motor", "kw": 37.0, "hp": 50.0, "poles": 4, "sync_rpm": 1500, "rated_rpm": 1475, "fla": 68.0, "app": "Extrusion Line"},
    "IM-106": {"name": "HVAC Chiller Pump", "kw": 18.5, "hp": 25.0, "poles": 4, "sync_rpm": 1500, "rated_rpm": 1465, "fla": 35.0, "app": "Chilled Water"},
    "IM-107": {"name": "Boiler Feed Water Pump", "kw": 45.0, "hp": 60.0, "poles": 2, "sync_rpm": 3000, "rated_rpm": 2960, "fla": 82.0, "app": "Steam Generation"}
}

features = ["temperature", "vibration", "current", "rpm", "pressure", "energy_consumption", "operating_hours"]

# Session State Setup
if "live_stream" not in st.session_state:
    st.session_state.live_stream = False
if "telemetry_index" not in st.session_state:
    st.session_state.telemetry_index = 0
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False
if "work_orders" not in st.session_state:
    st.session_state.work_orders = []

# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="padding: 6px 0 16px 0;">
            <div style="font-size: 1.15rem; font-weight: 800; color: #38bdf8; letter-spacing: 0.5px;">⚡ SCADA COCKPIT</div>
            <div style="font-size: 0.78rem; color: #94a3b8;">Induction Motor Digital Twin v2.5</div>
        </div>
    """, unsafe_allow_html=True)
    
    selected_machine = st.selectbox(
        "Select Active Motor",
        sorted(data["machine_id"].unique()),
        format_func=lambda m: f"{m} ({MOTOR_CATALOG.get(m, {}).get('name', 'Motor')})"
    )
    
    spec = MOTOR_CATALOG.get(selected_machine, {"name": "Motor", "kw": 15.0, "hp": 20.0, "poles": 4, "sync_rpm": 1500, "rated_rpm": 1460, "fla": 29.5, "app": "Industrial Drive"})
    
    st.markdown(f"""
        <div style="background: #131f33; padding: 12px; border-radius: 6px; border: 1px solid #233858; margin: 10px 0 16px 0; font-size: 0.80rem;">
            <div style="font-weight: 700; color: #f8fafc; margin-bottom: 4px;">{spec['name']}</div>
            <div style="color: #94a3b8; display: grid; grid-template-columns: 1fr 1fr; gap: 4px;">
                <span>Power: <b style="color:#ffffff;">{spec['kw']} kW</b></span>
                <span>Poles: <b style="color:#ffffff;">{spec['poles']} ({spec['sync_rpm']} RPM)</b></span>
                <span>FLA: <b style="color:#ffffff;">{spec['fla']} A</b></span>
                <span>Load App: <b style="color:#ffffff;">{spec['app']}</b></span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<b style='font-size:0.85rem; color:#e2e8f0;'>📡 Telemetry Stream Controller</b>", unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("▶ Start Stream", use_container_width=True, type="primary" if not st.session_state.live_stream else "secondary"):
            st.session_state.live_stream = True
            st.session_state.demo_mode = False
    with col_s2:
        if st.button("⏹ Pause Stream", use_container_width=True):
            st.session_state.live_stream = False
            
    stream_speed = st.slider("Update Rate (sec)", 1, 5, 2)
    
    st.markdown("---")
    st.markdown("<b style='font-size:0.85rem; color:#e2e8f0;'>🎬 Fault Injection Sandbox</b>", unsafe_allow_html=True)
    st.session_state.demo_mode = st.toggle("Enable Fault Simulator", value=st.session_state.demo_mode)
    
    if st.session_state.demo_mode:
        st.session_state.live_stream = False
        demo_choice = st.selectbox(
            "Select Scenario",
            [
                "Healthy Baseline (Normal)",
                "Stator Turn-to-Turn Short",
                "Broken Rotor Bars (BRB)",
                "Bearing Race Degradation",
                "Rotor Dynamic Eccentricity",
                "Thermal Overload & Blockage",
                "Phase Voltage Imbalance"
            ]
        )

# ==============================================================================
# TELEMETRY RETRIEVAL & INFERENCE ENGINE
# ==============================================================================
m_data = data[data["machine_id"] == selected_machine].reset_index(drop=True)
cur_idx = st.session_state.telemetry_index % len(m_data)
reading = m_data.iloc[cur_idx].copy()

# Apply Demo Scenario Overrides if Active
if st.session_state.demo_mode:
    if "Healthy" in demo_choice:
        reading["temperature"] = 58.0; reading["stator_temp"] = 58.0; reading["de_bearing_temp"] = 50.0; reading["vibration"] = 1.40; reading["current"] = 24.0; reading["rpm"] = 1465.0; reading["current_unbalance_pct"] = 1.2; reading["slip_pct"] = 2.33; reading["power_factor"] = 0.865; reading["fault_type"] = "Normal"
    elif "Stator Turn" in demo_choice:
        reading["temperature"] = 94.0; reading["stator_temp"] = 98.0; reading["de_bearing_temp"] = 64.0; reading["vibration"] = 2.65; reading["current"] = 35.5; reading["rpm"] = 1435.0; reading["current_unbalance_pct"] = 18.5; reading["slip_pct"] = 4.33; reading["power_factor"] = 0.740; reading["fault_type"] = "Stator Winding Inter-Turn Fault"
    elif "Broken Rotor" in demo_choice:
        reading["temperature"] = 76.0; reading["stator_temp"] = 78.0; reading["de_bearing_temp"] = 62.0; reading["vibration"] = 3.80; reading["current"] = 29.5; reading["rpm"] = 1390.0; reading["current_unbalance_pct"] = 6.8; reading["slip_pct"] = 7.33; reading["power_factor"] = 0.780; reading["fault_type"] = "Broken Rotor Bars"
    elif "Bearing Race" in demo_choice:
        reading["temperature"] = 74.0; reading["stator_temp"] = 72.0; reading["de_bearing_temp"] = 89.0; reading["vibration"] = 6.40; reading["current"] = 27.5; reading["rpm"] = 1450.0; reading["current_unbalance_pct"] = 2.4; reading["slip_pct"] = 3.33; reading["power_factor"] = 0.820; reading["fault_type"] = "Bearing Degradation"
    elif "Eccentricity" in demo_choice:
        reading["temperature"] = 72.0; reading["stator_temp"] = 74.0; reading["de_bearing_temp"] = 76.0; reading["vibration"] = 5.80; reading["current"] = 28.5; reading["rpm"] = 1420.0; reading["current_unbalance_pct"] = 5.8; reading["slip_pct"] = 5.33; reading["power_factor"] = 0.800; reading["fault_type"] = "Rotor Eccentricity & Misalignment"
    elif "Thermal Overload" in demo_choice:
        reading["temperature"] = 106.0; reading["stator_temp"] = 110.0; reading["de_bearing_temp"] = 86.0; reading["vibration"] = 3.20; reading["current"] = 41.0; reading["rpm"] = 1405.0; reading["current_unbalance_pct"] = 2.8; reading["slip_pct"] = 6.33; reading["power_factor"] = 0.875; reading["fault_type"] = "Thermal Overload & Cooling Blockage"
    elif "Phase Voltage" in demo_choice:
        reading["temperature"] = 89.0; reading["stator_temp"] = 93.0; reading["de_bearing_temp"] = 70.0; reading["vibration"] = 4.40; reading["current"] = 37.0; reading["rpm"] = 1415.0; reading["current_unbalance_pct"] = 23.5; reading["slip_pct"] = 5.67; reading["power_factor"] = 0.670; reading["fault_type"] = "Phase Imbalance & Supply Distortion"

# Model Inference
ai_in = pd.DataFrame([{f: reading[f] for f in features}])
fail_prob = float(failure_model.predict_proba(ai_in)[0][1] * 100.0)
mhi = float(max(0.0, min(100.0, 100.0 - fail_prob)))

if component_fault_model is not None:
    diag_class = component_fault_model.predict(ai_in)[0]
    diag_conf = float(max(component_fault_model.predict_proba(ai_in)[0]) * 100.0)
    diag_probs = dict(zip(component_fault_model.classes_, component_fault_model.predict_proba(ai_in)[0]))
else:
    diag_class = "Normal" if fail_prob < 40 else "Bearing Degradation"
    diag_conf = 85.0
    diag_probs = {}

# ISO 10816 Vibration Assessment
vib_val = reading["vibration"]
if vib_val < 1.4:
    iso_zone = "Zone A (Excellent)"; iso_badge = "badge-ok"
elif vib_val < 2.8:
    iso_zone = "Zone B (Good / Continuous)"; iso_badge = "badge-ok"
elif vib_val < 4.5:
    iso_zone = "Zone C (Warning / Plan Action)"; iso_badge = "badge-warn"
else:
    iso_zone = "Zone D (Critical / Trip)"; iso_badge = "badge-crit"

# Risk State
if fail_prob >= 70:
    overall_status = "CRITICAL / HIGH RISK"; status_badge = "badge-crit"
elif fail_prob >= 30:
    overall_status = "WARNING / MEDIUM RISK"; status_badge = "badge-warn"
else:
    overall_status = "NORMAL / HEALTHY"; status_badge = "badge-ok"

# ==============================================================================
# TOP SCADA HEADER
# ==============================================================================
st.markdown(f"""
<div class="scada-header">
    <div>
        <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff;">
            ⚡ {selected_machine} — {spec['name']} <span style="font-size: 0.95rem; font-weight: normal; color: #94a3b8;">({spec['kw']} kW | {spec['poles']}-Pole)</span>
        </div>
        <div style="font-size: 0.80rem; color: #94a3b8; margin-top: 4px;">
            Application: <b>{spec['app']}</b> | Synchronous Speed: <b>{spec['sync_rpm']} RPM</b> | Rated Current: <b>{spec['fla']} A</b>
        </div>
    </div>
    <div style="text-align: right;">
        <span class="badge {status_badge}" style="font-size: 0.88rem; padding: 6px 14px;">{overall_status}</span>
        <div style="font-size: 0.74rem; color: #64748b; margin-top: 4px;">Telemetry Sync: {datetime.now().strftime('%H:%M:%S')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# STREAMLINED 4-TAB ENGINEERING COCKPIT
# ==============================================================================
tab_cockpit, tab_diag, tab_physics, tab_sim, tab_fleet = st.tabs([
    "🎛️ Motor Cockpit",
    "🧠 AI Diagnostics & SOP",
    "⚡ Electromechanical Physics",
    "🧪 What-If Simulator",
    "📋 Fleet Overview & Reports"
])

# ==============================================================================
# TAB 1: MOTOR COCKPIT
# ==============================================================================
with tab_cockpit:
    # 6 Core Real-Time Telemetry Gauges
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(f"""<div class="telemetry-card"><div class="telemetry-label">Motor Health (MHI)</div><div class="telemetry-value" style="color:{'#34d399' if mhi>=70 else ('#fbbf24' if mhi>=40 else '#fb7185')};">{mhi:.1f}<span class="telemetry-unit">/100</span></div><div class="telemetry-sub">Failure Risk: {fail_prob:.1f}%</div></div>""", unsafe_allow_html=True)
    with c2:
        st_t = reading.get("stator_temp", reading["temperature"])
        st.markdown(f"""<div class="telemetry-card"><div class="telemetry-label">Stator Winding Temp</div><div class="telemetry-value" style="color:{'#fb7185' if st_t>88 else ('#fbbf24' if st_t>75 else '#ffffff')};">{st_t:.1f}<span class="telemetry-unit">°C</span></div><div class="telemetry-sub">Class F Limit: 105°C</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="telemetry-card"><div class="telemetry-label">DE Vibration (RMS)</div><div class="telemetry-value" style="color:{'#fb7185' if vib_val>4.5 else ('#fbbf24' if vib_val>2.8 else '#ffffff')};">{vib_val:.2f}<span class="telemetry-unit">mm/s</span></div><div class="telemetry-sub">{iso_zone.split('(')[0]}</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="telemetry-card"><div class="telemetry-label">Rotor Speed</div><div class="telemetry-value">{reading['rpm']:.0f}<span class="telemetry-unit">RPM</span></div><div class="telemetry-sub">Slip: {reading.get('slip_pct', 2.5):.2f}%</div></div>""", unsafe_allow_html=True)
    with c5:
        unbal = reading.get("current_unbalance_pct", 1.8)
        st.markdown(f"""<div class="telemetry-card"><div class="telemetry-label">Current Unbalance</div><div class="telemetry-value" style="color:{'#fb7185' if unbal>10 else ('#fbbf24' if unbal>5 else '#ffffff')};">{unbal:.1f}<span class="telemetry-unit">%</span></div><div class="telemetry-sub">Avg I: {reading['current']:.1f} A</div></div>""", unsafe_allow_html=True)
    with c6:
        st.markdown(f"""<div class="telemetry-card"><div class="telemetry-label">Active Power</div><div class="telemetry-value">{reading['energy_consumption']:.1f}<span class="telemetry-unit">kW</span></div><div class="telemetry-sub">cos φ: {reading.get('power_factor', 0.85):.2f}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2D Digital Twin Subsystem Status Block + Oscilloscope
    twin_col, osc_col = st.columns([1, 1.2])
    
    with twin_col:
        st.markdown("##### ⚙️ Subsystem Digital Twin Status")
        stator_ok = st_t <= 75
        bearing_ok = vib_val <= 2.8 and reading.get("de_bearing_temp", 60) <= 72
        rotor_ok = reading.get("slip_pct", 2.5) <= 4.0
        terminal_ok = unbal <= 5.0
        
        st.markdown(f"""
        <div class="subsystem-card" style="border-left: 4px solid {'#34d399' if stator_ok else ('#fbbf24' if st_t<=88 else '#fb7185')};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="color:#ffffff;">🌀 Stator Windings & Magnetic Core</b>
                <span class="badge {'badge-ok' if stator_ok else ('badge-warn' if st_t<=88 else 'badge-crit')}">{'NOMINAL' if stator_ok else ('WARN' if st_t<=88 else 'CRITICAL')}</span>
            </div>
            <div style="font-size:0.78rem; color:#94a3b8; margin-top:4px;">RTD Winding Temp: <b>{st_t:.1f}°C</b> | Insulation Stress: <b>{'Low' if stator_ok else 'High'}</b></div>
        </div>
        <div class="subsystem-card" style="border-left: 4px solid {'#34d399' if bearing_ok else ('#fbbf24' if vib_val<=4.5 else '#fb7185')};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="color:#ffffff;">⚙️ Drive-End (DE) & NDE Bearings</b>
                <span class="badge {'badge-ok' if bearing_ok else ('badge-warn' if vib_val<=4.5 else 'badge-crit')}">{'NOMINAL' if bearing_ok else ('WARN' if vib_val<=4.5 else 'CRITICAL')}</span>
            </div>
            <div style="font-size:0.78rem; color:#94a3b8; margin-top:4px;">DE Vibration: <b>{vib_val:.2f} mm/s</b> | DE Temp: <b>{reading.get('de_bearing_temp', 55):.1f}°C</b></div>
        </div>
        <div class="subsystem-card" style="border-left: 4px solid {'#34d399' if rotor_ok else ('#fbbf24' if reading.get('slip_pct', 2.5)<=6.0 else '#fb7185')};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="color:#ffffff;">🔄 Squirrel-Cage Rotor & End-Rings</b>
                <span class="badge {'badge-ok' if rotor_ok else ('badge-warn' if reading.get('slip_pct', 2.5)<=6.0 else 'badge-crit')}">{'NOMINAL' if rotor_ok else ('WARN' if reading.get('slip_pct', 2.5)<=6.0 else 'CRITICAL')}</span>
            </div>
            <div style="font-size:0.78rem; color:#94a3b8; margin-top:4px;">Rotor Speed: <b>{reading['rpm']:.0f} RPM</b> | Operating Slip: <b>{reading.get('slip_pct', 2.5):.2f}%</b></div>
        </div>
        <div class="subsystem-card" style="border-left: 4px solid {'#34d399' if terminal_ok else ('#fbbf24' if unbal<=10.0 else '#fb7185')};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="color:#ffffff;">⚡ Power Phase & Terminal Block</b>
                <span class="badge {'badge-ok' if terminal_ok else ('badge-warn' if unbal<=10.0 else 'badge-crit')}">{'BALANCED' if terminal_ok else 'UNBALANCED'}</span>
            </div>
            <div style="font-size:0.78rem; color:#94a3b8; margin-top:4px;">Current Unbalance: <b>{unbal:.1f}%</b> | Stator Current: <b>{reading['current']:.1f} A</b></div>
        </div>
        """, unsafe_allow_html=True)
        
    with osc_col:
        st.markdown("##### ⚡ 3-Phase Stator Current Oscilloscope (50Hz)")
        ir_val = reading.get("current_r", reading["current"])
        iy_val = reading.get("current_y", reading["current"])
        ib_val = reading.get("current_b", reading["current"])
        
        t_pts = np.linspace(0, 0.04, 150)
        w_r = ir_val * np.sqrt(2) * np.sin(2 * np.pi * 50.0 * t_pts)
        w_y = iy_val * np.sqrt(2) * np.sin(2 * np.pi * 50.0 * t_pts - (2*np.pi/3))
        w_b = ib_val * np.sqrt(2) * np.sin(2 * np.pi * 50.0 * t_pts + (2*np.pi/3))
        
        fig_w = go.Figure()
        fig_w.add_trace(go.Scatter(x=t_pts*1000, y=w_r, name="Phase R (U)", line=dict(color="#f43f5e", width=2)))
        fig_w.add_trace(go.Scatter(x=t_pts*1000, y=w_y, name="Phase Y (V)", line=dict(color="#f59e0b", width=2)))
        fig_w.add_trace(go.Scatter(x=t_pts*1000, y=w_b, name="Phase B (W)", line=dict(color="#38bdf8", width=2)))
        fig_w.update_layout(
            template="plotly_dark",
            height=260,
            margin=dict(l=15, r=15, t=10, b=15),
            xaxis_title="Time (ms)",
            yaxis_title="Current (A)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_w, use_container_width=True)

# ==============================================================================
# TAB 2: AI DIAGNOSTICS & SOP
# ==============================================================================
with tab_diag:
    st.subheader(f"🧠 AI Fault Diagnostics & Prescriptive SOP — {selected_machine}")
    
    d_c1, d_c2 = st.columns([1, 1.2])
    with d_c1:
        st.markdown(f"""
        <div style="background:#141f33; border: 1px solid #223450; border-radius:8px; padding:18px; border-left: 4px solid {'#fb7185' if fail_prob>=70 else ('#fbbf24' if fail_prob>=30 else '#34d399')};">
            <div style="font-size:0.80rem; text-transform:uppercase; color:#94a3b8; font-weight:700;">Primary AI Fault Diagnosis</div>
            <div style="font-size:1.45rem; font-weight:800; color:#ffffff; margin:6px 0;">{diag_class}</div>
            <div style="font-size:0.85rem; color:#94a3b8;">Confidence: <b style="color:#ffffff;">{diag_conf:.1f}%</b> | ISO 10816: <b style="color:#ffffff;">{iso_zone}</b></div>
            <div style="font-size:0.85rem; color:#94a3b8; margin-top:4px;">Failure Probability: <b style="color:{'#fb7185' if fail_prob>=70 else ('#fbbf24' if fail_prob>=30 else '#34d399')};">{fail_prob:.1f}%</b></div>
        </div>
        """, unsafe_allow_html=True)
        
        if diag_probs:
            fig_p = px.bar(
                x=list(diag_probs.values()),
                y=list(diag_probs.keys()),
                orientation='h',
                labels={'x': 'Probability', 'y': 'Fault Mode'},
                title="Fault Mode Class Probabilities",
                color=list(diag_probs.values()),
                color_continuous_scale="Teal"
            )
            fig_p.update_layout(template="plotly_dark", height=240, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_p, use_container_width=True)
            
    with d_c2:
        # SOP Action Card
        sop_map = {
            "Normal": ("Routine Maintenance Protocol", "P4 - Normal", ["Maintain scheduled periodic lubrication schedule.", "Log monthly vibration and thermal baselines.", "Verify cooling fins remain clean."]),
            "Stator Winding Inter-Turn Fault": ("Stator Turn-to-Turn Isolation Protocol", "P1 - Critical", ["Perform Lockout/Tagout (LOTO) and de-energize motor.", "Measure DC winding resistance balance with micro-ohmmeter (< 2%).", "Conduct 1000V DC Megger & Surge Comparison test.", "Inspect stator end-turns for localized burning / insulation breakdown."]),
            "Broken Rotor Bars": ("Rotor Bar Integrity & MCSA Protocol", "P2 - High", ["Perform High-Resolution MCSA around (1±2s)fs fundamental sidebands.", "Conduct single-phase low-voltage slow rotation test to detect torque dips.", "Inspect rotor end-ring braze joints for thermal fatigue cracks."]),
            "Bearing Degradation": ("Bearing Re-grease / Replacement SOP", "P1 - Critical", ["Measure shock pulse / crest factor on DE and NDE housings.", "Inspect grease condition for particulate contamination or saponification.", "Inject specified Polyurea/Lithium EP2 grease.", "If vibration > 4.5 mm/s persists, replace bearing assembly (SKF 6309 C3)."]),
            "Rotor Eccentricity & Misalignment": ("Shaft Laser Alignment & Air-Gap Calibration", "P2 - High", ["Measure stator-rotor air-gap at 4 quadrant points (deviation < 10%).", "Check motor mounting base for soft-foot (< 0.05 mm).", "Perform dual-laser shaft alignment with driven equipment."]),
            "Thermal Overload & Cooling Blockage": ("Thermal Airflow Restoration", "P2 - High", ["Clear dust and debris from cooling fan cowl and stator fins.", "Inspect cooling fan impeller for broken blades.", "Verify driven equipment mechanical load does not exceed motor rating."]),
            "Phase Imbalance & Supply Distortion": ("Power Quality & Switchgear Inspection", "P1 - Critical", ["Measure line voltages to verify voltage unbalance < 1% (NEMA MG-1).", "Inspect contactor and breaker main contacts for pitting.", "Check capacitor banks and supply transformer tap settings."])
        }
        title, priority, acts = sop_map.get(diag_class, sop_map["Normal"])
        
        st.markdown(f"""
        <div style="background:#141f33; border: 1px solid #223450; border-radius:8px; padding:18px; border-top: 3px solid #38bdf8;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <b style="color:#ffffff; font-size:1.05rem;">🛠️ Prescriptive Engineering SOP: {title}</b>
                <span class="badge badge-warn">{priority}</span>
            </div>
            <div style="margin-top:12px; font-size:0.82rem; color:#cbd5e1;">
                <b style="color:#f8fafc;">Standard Operating Procedures:</b>
                <ul style="margin:6px 0 0 0; padding-left:18px;">
                    {''.join([f'<li style="margin-bottom:4px;">{a}</li>' for a in acts])}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Dispatch Maintenance Work Order", use_container_width=True):
            st.session_state.work_orders.append({
                "time": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "machine": selected_machine,
                "fault": diag_class,
                "priority": priority
            })
            st.success(f"✓ Work Order dispatched for {selected_machine}!")

# ==============================================================================
# TAB 3: ELECTROMECHANICAL PHYSICS & TORQUE-SPEED
# ==============================================================================
with tab_physics:
    st.subheader(f"⚡ Electromechanical Physics & Kloss Torque Curve — {selected_machine}")
    
    rated_kw = spec["kw"]
    sync_rpm = spec["sync_rpm"]
    rated_rpm = spec["rated_rpm"]
    
    # Kloss Equation
    w_sync = (2 * np.pi * sync_rpm) / 60.0
    T_rated = (rated_kw * 1000.0) / ((2 * np.pi * rated_rpm) / 60.0)
    T_max = 2.4 * T_rated
    s_max = 0.12
    
    sp_arr = np.linspace(0, sync_rpm, 150)
    sl_arr = np.clip((sync_rpm - sp_arr) / sync_rpm, 1e-4, 1.0)
    t_ideal = (2.0 * T_max) / ((sl_arr / s_max) + (s_max / sl_arr))
    
    cur_rpm = reading["rpm"]
    cur_w = (2 * np.pi * max(100.0, cur_rpm)) / 60.0
    cur_t = (reading["energy_consumption"] * 1000.0 * (reading.get("efficiency_pct", 90.0)/100.0)) / cur_w
    
    p_c1, p_c2 = st.columns([1.3, 1])
    with p_c1:
        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(x=sp_arr, y=t_ideal, name="Ideal Torque (N·m)", line=dict(color="#10b981", width=2)))
        fig_t.add_trace(go.Scatter(x=[cur_rpm], y=[cur_t], mode="markers+text", name="Live Operating Point", text=[f"{cur_rpm:.0f} RPM, {cur_t:.1f} N·m"], textposition="top right", marker=dict(size=12, color="#38bdf8", symbol="diamond")))
        fig_t.add_vline(x=sync_rpm, line_dash="dot", line_color="#64748b", annotation_text=f"Sync: {sync_rpm}")
        fig_t.update_layout(
            title=f"Kloss Torque-Speed Curve (Rated: {T_rated:.1f} N·m | Breakdown: {T_max:.1f} N·m)",
            xaxis_title="Rotor Speed (RPM)",
            yaxis_title="Torque (N·m)",
            template="plotly_dark",
            height=280,
            margin=dict(l=15, r=15, t=35, b=15),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_t, use_container_width=True)
        
    with p_c2:
        # Loss Breakdown
        p_in = reading["energy_consumption"]
        eff = reading.get("efficiency_pct", 90.0) / 100.0
        p_out = p_in * eff
        p_loss = p_in - p_out
        
        fig_l = px.pie(
            values=[p_out, p_loss*0.35, p_loss*0.25, p_loss*0.20, p_loss*0.20],
            names=["Useful Mech Output", "Stator I²R Cu Loss", "Rotor I²R Cu Loss", "Core Iron Loss", "Friction & Stray"],
            title=f"Active Power Dissipation ({p_in:.1f} kW)",
            color_discrete_sequence=["#10b981", "#f43f5e", "#f59e0b", "#38bdf8", "#818cf8"],
            hole=0.45
        )
        fig_l.update_layout(template="plotly_dark", height=280, margin=dict(l=10, r=10, t=35, b=10), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_l, use_container_width=True)

# ==============================================================================
# TAB 4: WHAT-IF SIMULATOR
# ==============================================================================
with tab_sim:
    st.subheader("🧪 Interactive Induction Motor Simulator")
    st.caption("Adjust mechanical and electrical operating points to observe real-time AI diagnostic response.")
    
    s_col1, s_col2 = st.columns([1, 1.2])
    with s_col1:
        sim_temp = st.slider("Stator Temperature (°C)", 30.0, 120.0, float(st_t), 1.0)
        sim_vib = st.slider("DE Vibration (mm/s RMS)", 0.5, 9.0, float(vib_val), 0.1)
        sim_curr = st.slider("Stator Current (A)", 5.0, 80.0, float(reading["current"]), 0.5)
        sim_rpm = st.slider("Rotor Speed (RPM)", 1000.0, 3000.0, float(reading["rpm"]), 10.0)
        sim_hours = st.slider("Operating Hours (hrs)", 500.0, 6000.0, float(reading["operating_hours"]), 50.0)
        
    with s_col2:
        sim_in = pd.DataFrame([{
            "temperature": sim_temp,
            "vibration": sim_vib,
            "current": sim_curr,
            "rpm": sim_rpm,
            "pressure": 3.3,
            "energy_consumption": 16.5,
            "operating_hours": sim_hours
        }])
        s_prob = float(failure_model.predict_proba(sim_in)[0][1] * 100.0)
        s_mhi = float(max(0.0, min(100.0, 100.0 - s_prob)))
        s_diag = component_fault_model.predict(sim_in)[0] if component_fault_model else "Normal"
        
        st.markdown(f"""
        <div style="background:#141f33; border: 1px solid #223450; border-radius:8px; padding:18px;">
            <div style="font-size:0.80rem; text-transform:uppercase; color:#94a3b8; font-weight:700;">Simulated Diagnostic State</div>
            <div style="display:flex; justify-content:space-between; margin-top:10px;">
                <span>Simulated Health (MHI):</span>
                <b style="color:{'#34d399' if s_mhi>=70 else ('#fbbf24' if s_mhi>=40 else '#fb7185')};">{s_mhi:.1f} / 100</b>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:8px;">
                <span>Failure Risk:</span>
                <b style="color:{'#fb7185' if s_prob>=70 else ('#fbbf24' if s_prob>=30 else '#34d399')};">{s_prob:.1f}%</b>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:8px;">
                <span>Diagnosed Fault Mode:</span>
                <b style="color:#ffffff;">{s_diag}</b>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:8px;">
                <span>Operating Decision:</span>
                <b style="color:{'#fb7185' if s_prob>=failure_threshold*100 else '#34d399'};">{'🚨 SHUTDOWN / TRIP' if s_prob>=failure_threshold*100 else '✅ NORMAL RUN'}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 5: FLEET OVERVIEW & REPORT EXPORT
# ==============================================================================
with tab_fleet:
    st.subheader("📋 Plant-Wide Fleet Manager & Certified Report Export")
    
    # Fleet Summary Table
    fl_list = []
    for m in sorted(data["machine_id"].unique()):
        row_m = data[data["machine_id"] == m].iloc[-1]
        in_m = pd.DataFrame([{f: row_m[f] for f in features}])
        fp = failure_model.predict_proba(in_m)[0][1] * 100.0
        fl_list.append({
            "Motor ID": m,
            "Machine Name": MOTOR_CATALOG.get(m, {}).get("name", "Motor"),
            "Power (kW)": MOTOR_CATALOG.get(m, {}).get("kw", 15.0),
            "Temp (°C)": row_m["temperature"],
            "Vib (mm/s)": row_m["vibration"],
            "Speed (RPM)": row_m["rpm"],
            "Health (%)": round(100.0 - fp, 1),
            "Status": "HIGH RISK" if fp>=70 else ("WARNING" if fp>=30 else "NORMAL")
        })
    fl_df = pd.DataFrame(fl_list)
    st.dataframe(fl_df, use_container_width=True)
    
    st.markdown("---")
    
    # Certified Report Download
    rep = f"""================================================================================
SMART INDUSTRY AI — INDUCTION MOTOR DIAGNOSTIC REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================
Motor Asset   : {selected_machine} ({spec['name']})
Application   : {spec['app']} | Rating: {spec['kw']} kW ({spec['hp']} HP) | Poles: {spec['poles']}
Health Index  : {mhi:.1f} / 100 | Risk: {overall_status}
Diagnosis     : {diag_class} (Confidence: {diag_conf:.1f}%)
ISO 10816-3   : {iso_zone} (Vibration: {vib_val:.2f} mm/s RMS)
Stator Temp   : {st_t:.1f} °C | Current: {reading['current']:.1f} A | RPM: {reading['rpm']:.0f}
================================================================================
"""
    st.download_button(
        "📥 Export Certified Diagnostic Report (TXT)",
        rep,
        file_name=f"Report_{selected_machine}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
        use_container_width=True
    )

# ==============================================================================
# LIVE STREAM RUNNER
# ==============================================================================
if st.session_state.live_stream:
    time.sleep(stream_speed)
    st.session_state.telemetry_index += 1
    st.rerun()