import pandas as pd
import numpy as np

# ==============================================================================
# SMART INDUSTRY AI - INDUCTION MACHINE ENERGY & EFFICIENCY ANALYZER
# ==============================================================================
# Analyzes electrical efficiency, power factor penalties, energy losses, 
# and carbon emissions (CO2) for 3-Phase Induction Motors under IEC 60034-30-1.
# ==============================================================================

data = pd.read_csv("data/industrial_dataset.csv")

print("==========================================================")
print(" SMART INDUSTRY AI - INDUCTION MOTOR ENERGY ANALYZER")
print("==========================================================")

# Average metrics across fleet
avg_kw = data["energy_consumption"].mean()
avg_pf = data["power_factor"].mean() if "power_factor" in data.columns else 0.84
avg_eff = data["efficiency_pct"].mean() if "efficiency_pct" in data.columns else 88.5

print(f"\nFleet Overview:")
print(f"  • Total Active Power Avg : {avg_kw:.2f} kW")
print(f"  • Average Operating PF   : {avg_pf:.3f}")
print(f"  • Average Motor Efficiency: {avg_eff:.2f}% (IEC 60034 Standard)")

# Machine-wise energy breakdown
summary = data.groupby("machine_id").agg({
    "energy_consumption": "mean",
    "power_factor": "mean",
    "efficiency_pct": "mean",
    "load_pct": "mean",
    "stator_temp": "mean"
}).reset_index()

summary.columns = [
    "Machine ID",
    "Avg Power (kW)",
    "Power Factor",
    "Efficiency (%)",
    "Avg Load (%)",
    "Avg Temp (°C)"
]

# Estimate annual electricity cost & CO2 footprint (Assuming 6,000 operational hrs/year, $0.12/kWh, 0.75 kg CO2/kWh)
summary["Annual kWh"] = summary["Avg Power (kW)"] * 6000
summary["Annual Cost ($)"] = summary["Annual kWh"] * 0.12
summary["Annual CO2 (Tons)"] = (summary["Annual kWh"] * 0.75) / 1000.0

print("\n========== MACHINE-WISE ENERGY & EFFICIENCY TABLE ==========")
print(summary.to_string(index=False))

# Identify low power factor or high thermal loss machines
low_pf_machines = summary[summary["Power Factor"] < 0.82]
if len(low_pf_machines) > 0:
    print("\n⚠️ Machines with Low Power Factor (< 0.82) - Penalty Risk:")
    for _, row in low_pf_machines.iterrows():
        print(f"  • {row['Machine ID']}: PF={row['Power Factor']:.3f} | Efficiency={row['Efficiency (%)']:.1f}%")

print("\n==========================================================")
print("               ENERGY ANALYSIS COMPLETE")
print("==========================================================")