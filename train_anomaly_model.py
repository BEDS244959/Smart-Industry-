import pandas as pd
import joblib
import os

from sklearn.ensemble import IsolationForest


# ==================================================
# SMART INDUSTRY AI - ANOMALY MODEL TRAINING
# ==================================================

print()
print("==============================================")
print("     SMART INDUSTRY AI - ANOMALY TRAINING")
print("==============================================")


# ==================================================
# LOAD DATA
# ==================================================

data = pd.read_csv(
    "data/industrial_dataset.csv"
)

print()
print("Dataset loaded successfully!")

print(
    "Total readings:",
    len(data)
)

print(
    "Total machines:",
    data["machine_id"].nunique()
)


# ==================================================
# SELECT FEATURES
# ==================================================

features = [

    "temperature",

    "vibration",

    "current",

    "rpm",

    "pressure",

    "energy_consumption",

    "operating_hours"
]


X = data[features]


print()
print("Features used by anomaly detector:")

for feature in features:

    print(
        "-",
        feature
    )


# ==================================================
# CREATE ISOLATION FOREST
# ==================================================

print()
print("==============================================")
print("CREATING ANOMALY DETECTION MODEL")
print("==============================================")


model = IsolationForest(

    n_estimators=200,

    contamination=0.05,

    random_state=42,

    n_jobs=-1
)


# ==================================================
# TRAIN MODEL
# ==================================================

print()
print("Training anomaly detection model...")

model.fit(
    X
)

print(
    "Anomaly detection model training completed!"
)


# ==================================================
# DETECT ANOMALIES
# ==================================================

predictions = model.predict(
    X
)


# Isolation Forest:
#  1  = NORMAL
# -1  = ANOMALY

normal_count = (
    predictions == 1
).sum()


anomaly_count = (
    predictions == -1
).sum()


# ==================================================
# DISPLAY RESULTS
# ==================================================

print()
print("==============================================")
print("ANOMALY RESULTS")
print("==============================================")


print(
    "Normal readings:",
    normal_count
)


print(
    "Anomalous readings:",
    anomaly_count
)


print(
    "Total readings:",
    len(predictions)
)


print(
    "Anomaly percentage:",
    round(
        anomaly_count
        / len(predictions)
        * 100,
        2
    ),
    "%"
)


# ==================================================
# MACHINE-WISE ANOMALIES
# ==================================================

data["anomaly"] = predictions


machine_anomalies = (
    data[data["anomaly"] == -1]
    .groupby("machine_id")
    .size()
    .sort_values(
        ascending=False
    )
)


print()
print("==============================================")
print("MACHINE-WISE ANOMALIES")
print("==============================================")


if len(machine_anomalies) > 0:

    print(
        machine_anomalies
    )

else:

    print(
        "No anomalies detected."
    )


# ==================================================
# CREATE MODELS FOLDER
# ==================================================

os.makedirs(
    "models",
    exist_ok=True
)


# ==================================================
# SAVE MODEL
# ==================================================

model_path = (
    "models/anomaly_detection_model.pkl"
)


joblib.dump(
    model,
    model_path
)


print()
print("==============================================")
print("MODEL SAVING")
print("==============================================")


print(
    "Anomaly model saved successfully!"
)


print(
    "Location:",
    model_path
)


# ==================================================
# COMPLETE
# ==================================================

print()
print("==============================================")
print("     ANOMALY TRAINING COMPLETE")
print("==============================================")