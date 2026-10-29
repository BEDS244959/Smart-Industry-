import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configure high-resolution publication styling
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 12

os.makedirs("figures", exist_ok=True)
print("Generating publication-ready figures at 300 DPI...")

# ==============================================================================
# FIGURE 1: CONFUSION MATRIX HEATMAP
# ==============================================================================
fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
classes = [
    "Normal",
    "Stator Fault",
    "Broken Rotor",
    "Bearing Deg.",
    "Eccentricity",
    "Thermal Over.",
    "Phase Imbal."
]
cm = np.array([
    [140,   0,   0,   0,   0,   0,   0],
    [  0, 133,   0,   0,   0,   0,   7],
    [  0,   2, 129,   4,   4,   0,   1],
    [  0,   0,   5, 118,  17,   0,   0],
    [  0,   0,   9,  22, 109,   0,   0],
    [  0,   0,   0,   0,   0, 140,   0],
    [  0,   8,   4,   0,   1,   0, 127]
])

im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

ax.set(xticks=np.arange(cm.shape[1]),
       yticks=np.arange(cm.shape[0]),
       xticklabels=classes, yticklabels=classes,
       ylabel='True Operational Class',
       xlabel='Predicted Diagnostic Class')

plt.setp(ax.get_xticklabels(), rotation=35, ha="right", rotation_mode="anchor")

thresh = cm.max() / 2.
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j, i, format(cm[i, j], 'd'),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black",
                fontweight='bold' if cm[i, j] > 0 else 'normal')

fig.tight_layout()
plt.savefig("figures/fig_confusion_matrix.png", dpi=300)
plt.close()
print("Saved figures/fig_confusion_matrix.png")

# ==============================================================================
# FIGURE 2: KLOSS TORQUE-SPEED & DERATING CURVE
# ==============================================================================
fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)
sync_rpm = 1500.0
rated_rpm = 1460.0
speed = np.linspace(0, sync_rpm, 250)
slip = np.clip((sync_rpm - speed) / sync_rpm, 1e-4, 1.0)

T_rated = 98.1 # N.m for 15kW motor
T_max = 2.4 * T_rated
s_max = 0.12

# Kloss equation
torque_healthy = (2.0 * T_max) / ((slip / s_max) + (s_max / slip))
torque_fault = torque_healthy * 0.72 # Stator turn short derating

ax.plot(speed, torque_healthy, 'g-', lw=2.2, label='Nominal Healthy Envelope (Kloss Model)')
ax.plot(speed, torque_fault, 'r--', lw=2.0, label='Derated Envelope (Stator Inter-Turn Fault)')

# Operating points
ax.scatter([1460], [T_rated], color='blue', s=80, zorder=5, label='Rated Operating Point (1460 RPM, 98.1 N·m)')
ax.scatter([1435], [T_rated * 0.95], color='red', marker='X', s=90, zorder=5, label='Fault Operating Point (Elevated Slip)')

ax.axvline(x=sync_rpm, color='gray', linestyle=':', label='Synchronous Speed $N_s$ (1500 RPM)')
ax.axhline(y=T_max, color='orange', linestyle='-.', alpha=0.7, label=f'Breakdown Torque $T_{{max}}$ ({T_max:.1f} N·m)')

ax.set_xlabel('Rotor Shaft Speed $N_r$ (RPM)')
ax.set_ylabel('Electromechanical Torque $T_e$ (N·m)')
ax.set_xlim(0, 1600)
ax.set_ylim(0, 260)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(loc='upper left', framealpha=0.9, fontsize=8)

fig.tight_layout()
plt.savefig("figures/fig_torque_speed.png", dpi=300)
plt.close()
print("Saved figures/fig_torque_speed.png")

# ==============================================================================
# FIGURE 3: 3-PHASE CURRENT OSCILLOSCOPE & MCSA SPECTRUM
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8), dpi=300)

# 3.1 Time domain 3-phase current
t = np.linspace(0, 0.04, 300) # 2 complete 50Hz cycles
I_peak = 29.5 * np.sqrt(2)
i_r = I_peak * np.sin(2 * np.pi * 50 * t)
i_y = (I_peak * 0.85) * np.sin(2 * np.pi * 50 * t - 2*np.pi/3) # Stator turn imbalance
i_b = I_peak * np.sin(2 * np.pi * 50 * t + 2*np.pi/3)

ax1.plot(t * 1000, i_r, 'r-', lw=1.8, label='Phase R (Faulted: 41.7 A pk)')
ax1.plot(t * 1000, i_y, 'goldenrod', lw=1.8, label='Phase Y (35.4 A pk)')
ax1.plot(t * 1000, i_b, 'b-', lw=1.8, label='Phase B (41.7 A pk)')
ax1.set_title('(a) 3-Phase Stator Current under Imbalance', fontsize=10)
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Instantaneous Current (A)')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='lower right', fontsize=8)

# 3.2 MCSA Frequency Spectrum
f = np.linspace(35, 65, 300)
s = 0.045
sb_l = 50 * (1 - 2*s) # 45.5 Hz
sb_r = 50 * (1 + 2*s) # 54.5 Hz

carrier = 60 * np.exp(-0.5 * ((f - 50)/0.4)**2)
sideband_l = 32 * np.exp(-0.5 * ((f - sb_l)/0.35)**2)
sideband_r = 30 * np.exp(-0.5 * ((f - sb_r)/0.35)**2)
noise = np.random.normal(4, 0.5, len(f))
spectrum = carrier + sideband_l + sideband_r + noise

ax2.plot(f, spectrum, 'teal', lw=1.6)
ax2.fill_between(f, spectrum, color='teal', alpha=0.2)
ax2.axvline(x=50, color='crimson', linestyle='--', label='Carrier $f_s$ (50 Hz)')
ax2.axvline(x=sb_l, color='purple', linestyle=':', label='$(1-2s)f_s$ Sideband (45.5 Hz)')
ax2.axvline(x=sb_r, color='purple', linestyle=':', label='$(1+2s)f_s$ Sideband (54.5 Hz)')
ax2.set_title('(b) MCSA Spectrum: Broken Rotor Bar Sidebands', fontsize=10)
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Spectral Magnitude (dB)')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='upper right', fontsize=8)

fig.tight_layout()
plt.savefig("figures/fig_mcsa_oscilloscope.png", dpi=300)
plt.close()
print("Saved figures/fig_mcsa_oscilloscope.png")

# ==============================================================================
# FIGURE 4: DECISION THRESHOLD TRADEOFF & GINI ATTRIBUTION
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.0), dpi=300)

# 4.1 Decision Threshold Sweep
thresholds = [0.20, 0.25, 0.30, 0.40, 0.50]
prec = [38.86, 41.71, 44.57, 54.17, 57.63]
rec = [92.71, 91.67, 85.42, 81.25, 70.83]
f1 = [54.77, 57.33, 58.57, 65.00, 63.55]

ax1.plot(thresholds, prec, 'b-o', lw=2, label='Precision (%)')
ax1.plot(thresholds, rec, 'r-s', lw=2, label='Recall (%)')
ax1.plot(thresholds, f1, 'g-^', lw=2.2, label='F1-Score (%)')
ax1.axvline(x=0.40, color='black', linestyle='--', lw=1.5, label='Selected Threshold $\\theta = 0.40$')
ax1.set_title('(a) Binary Failure Classifier Threshold Tuning', fontsize=10)
ax1.set_xlabel('Decision Probability Threshold ($\\theta$)')
ax1.set_ylabel('Metric Score (%)')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='center left', fontsize=8)

# 4.2 Feature Importance Ranking
features = ['Vibration RMS', 'Stator Temp', 'Rotor Speed', 'Current RMS', 'Active Power', 'Op. Hours', 'Coolant Press.']
weights = [35.96, 21.89, 9.83, 9.21, 9.17, 7.13, 6.82]

y_pos = np.arange(len(features))
ax2.barh(y_pos, weights[::-1], color='#38bdf8', edgecolor='#0284c7', height=0.6)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(features[::-1])
ax2.set_title('(b) Gini Feature Importance Attribution', fontsize=10)
ax2.set_xlabel('Relative Weight (%)')
for i, v in enumerate(weights[::-1]):
    ax2.text(v + 0.8, i - 0.1, f"{v:.1f}%", color='#0f172a', fontweight='bold', fontsize=8)
ax2.set_xlim(0, 42)
ax2.grid(True, axis='x', linestyle='--', alpha=0.5)

fig.tight_layout()
plt.savefig("figures/fig_threshold_and_features.png", dpi=300)
plt.close()
print("Saved figures/fig_threshold_and_features.png")

# ==============================================================================
# FIGURE 5: DIGITAL TWIN PROTOTYPE ARCHITECTURE & SCADA UI
# ==============================================================================
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
ax.axis('off')

# Background
ax.add_patch(patches.FancyBboxPatch((0.02, 0.05), 0.96, 0.90, boxstyle="round,pad=0.02", fc="#0b1120", ec="#243552", lw=2))

# Title bar
ax.text(0.06, 0.88, "SCADA DIGITAL TWIN COCKPIT - INDUCTION MACHINE [IM-101: 15 kW, 4-Pole]", 
        color="#38bdf8", fontsize=11, fontweight='bold')
ax.text(0.06, 0.83, "IEEE 841 / ISO 10816-3 Condition Monitoring | Real-Time Telemetry & Prescriptive Work Orders", 
        color="#94a3b8", fontsize=8)

# Telemetry KPI Boxes
kpis = [
    ("MHI HEALTH", "76.0/100", "#10b981"),
    ("STATOR TEMP", "78.5 °C", "#f59e0b"),
    ("DE VIBRATION", "4.65 mm/s", "#f43f5e"),
    ("ROTOR SPEED", "1410 RPM", "#38bdf8"),
    ("CURRENT UNBAL.", "12.4 %", "#f43f5e"),
    ("ACTIVE POWER", "18.5 kW", "#38bdf8")
]

for idx, (title, val, col) in enumerate(kpis):
    x = 0.06 + idx * 0.147
    ax.add_patch(patches.FancyBboxPatch((x, 0.65), 0.135, 0.14, boxstyle="round,pad=0.01", fc="#152238", ec=col, lw=1.5))
    ax.text(x + 0.067, 0.74, title, color="#8fa2be", fontsize=6.5, ha='center', fontweight='bold')
    ax.text(x + 0.067, 0.68, val, color=col, fontsize=9.5, ha='center', fontweight='bold')

# Lower panels
# Subsystem panel
ax.add_patch(patches.FancyBboxPatch((0.06, 0.12), 0.42, 0.48, boxstyle="round,pad=0.01", fc="#131d31", ec="#233a63", lw=1.5))
ax.text(0.08, 0.55, "PHYSICAL SUBSYSTEM HEALTH MAP", color="#38bdf8", fontsize=8.5, fontweight='bold')
subsystems = [
    ("Stator Windings & Core", "78.5°C [RESTRICTED]", "#f59e0b"),
    ("Drive-End (DE) Bearing", "4.65 mm/s [ISO ZONE D CRITICAL]", "#f43f5e"),
    ("Squirrel-Cage Rotor", "Slip: 6.00% [BRB SIDEBANDS DETECTED]", "#f43f5e"),
    ("Terminal Phase Bus", "Unbalance: 12.4% [VOLTAGE DISTORTION]", "#f59e0b")
]
for i, (name, status, sc) in enumerate(subsystems):
    y = 0.46 - i * 0.09
    ax.add_patch(patches.FancyBboxPatch((0.08, y), 0.38, 0.07, boxstyle="round,pad=0.005", fc="#1c2b46", ec=sc, lw=1))
    ax.text(0.10, y + 0.022, f"• {name}: {status}", color="#f1f5f9", fontsize=7.2, fontweight='bold')

# Prescriptive SOP panel
ax.add_patch(patches.FancyBboxPatch((0.52, 0.12), 0.42, 0.48, boxstyle="round,pad=0.01", fc="#131d31", ec="#233a63", lw=1.5))
ax.text(0.54, 0.55, "PRESCRIPTIVE MAINTENANCE WORK ORDER", color="#10b981", fontsize=8.5, fontweight='bold')
ax.text(0.54, 0.50, "Diagnosis: Stator Turn Short + Bearing Degradation (P1)", color="#f43f5e", fontsize=7.5, fontweight='bold')
sops = [
    "1. Lockout/Tagout (LOTO) & isolate 400V motor supply.",
    "2. Measure DC winding resistance balance (micro-ohmmeter < 2%).",
    "3. Perform 1000V DC Megger & Surge Comparison test.",
    "4. Check DE bearing housing for race spalling & purge grease.",
    "5. Target turnaround resolution: Within 8 to 12 Hours."
]
for j, step in enumerate(sops):
    ax.text(0.54, 0.43 - j * 0.065, step, color="#cbd5e1", fontsize=7.0)

fig.tight_layout()
plt.savefig("figures/fig_prototype_scada.png", dpi=300)
plt.close()
print("Saved figures/fig_prototype_scada.png")

print("All publication figures successfully created in figures/ directory!")
