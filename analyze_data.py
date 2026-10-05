import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# LOAD DATA
# ==================================================

data = pd.read_csv("data/industrial_dataset.csv")

print("========== SMART INDUSTRY AI ==========")
print()

# ==================================================
# BASIC INFORMATION
# ==================================================

print("========== BASIC INFORMATION ==========")

print("Total readings:", len(data))
print("Number of machines:", data["machine_id"].nunique())
print("Number of features:", len(data.columns))

# ==================================================
# COLUMNS
# ==================================================

print()
print("========== COLUMNS ==========")

print(data.columns.tolist())

# ==================================================
# FIRST FIVE READINGS
# ==================================================

print()
print("========== FIRST 5 READINGS ==========")

print(data.head())

# ==================================================
# MACHINE COUNTS
# ==================================================

print()
print("========== MACHINE COUNTS ==========")

machine_counts = data["machine_id"].value_counts().sort_index()

print(machine_counts)

# ==================================================
# FAILURE COUNTS
# ==================================================

print()
print("========== FAILURE COUNTS ==========")

failure_counts = data["failure"].value_counts()

print(failure_counts)

# ==================================================
# MAINTENANCE COUNTS
# ==================================================

print()
print("========== MAINTENANCE COUNTS ==========")

maintenance_counts = data["maintenance_required"].value_counts()

print(maintenance_counts)

# ==================================================
# MACHINE-WISE FAILURES
# ==================================================

print()
print("========== MACHINE-WISE FAILURES ==========")

machine_failures = data.groupby("machine_id")["failure"].sum()

print(machine_failures)

# ==================================================
# MACHINE-WISE MAINTENANCE
# ==================================================

print()
print("========== MACHINE-WISE MAINTENANCE ==========")

machine_maintenance = data.groupby("machine_id")[
    "maintenance_required"
].sum()

print(machine_maintenance)

# ==================================================
# AVERAGE MACHINE VALUES
# ==================================================

print()
print("========== AVERAGE MACHINE VALUES ==========")

average_values = data[
    [
        "temperature",
        "vibration",
        "current",
        "rpm",
        "pressure",
        "energy_consumption",
        "operating_hours"
    ]
].mean()

print(average_values)

# ==================================================
# MACHINE-WISE AVERAGES
# ==================================================

print()
print("========== MACHINE-WISE AVERAGES ==========")

machine_averages = data.groupby("machine_id")[
    [
        "temperature",
        "vibration",
        "current",
        "rpm",
        "pressure",
        "energy_consumption"
    ]
].mean()

print(machine_averages.round(2))

# ==================================================
# GRAPH 1 — AVERAGE TEMPERATURE
# ==================================================

print()
print("Creating temperature graph...")

average_temperature = data.groupby("machine_id")[
    "temperature"
].mean()

plt.figure(figsize=(8, 5))

plt.bar(
    average_temperature.index,
    average_temperature.values
)

plt.title("Average Temperature by Machine")
plt.xlabel("Machine")
plt.ylabel("Temperature (°C)")

plt.tight_layout()

plt.show()

print()
print("========== ANALYSIS COMPLETE ==========")