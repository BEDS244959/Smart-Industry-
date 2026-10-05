import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# =========================================================
# SMART INDUSTRY AI
# COMPONENT FAULT MODEL TRAINING
# =========================================================

print()
print("==============================================")
print("SMART INDUSTRY AI")
print("COMPONENT FAULT AI MODEL TRAINING")
print("==============================================")
print()


# =========================================================
# LOAD DATASET
# =========================================================

data = pd.read_csv(
    "data/component_fault_dataset.csv"
)


print("Dataset loaded successfully.")
print("Total samples:", len(data))
print()


# =========================================================
# FEATURES
# =========================================================

features = [

    "temperature",

    "vibration",

    "current",

    "rpm",

    "pressure",

    "energy_consumption",

    "operating_hours"
]


target = "fault_type"


# =========================================================
# PREPARE X AND Y
# =========================================================

X = data[features]

y = data[target]


print("Features used:")

for feature in features:
    print(" -", feature)

print()


# =========================================================
# TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("Training samples:", len(X_train))

print("Testing samples:", len(X_test))

print()


# =========================================================
# RANDOM FOREST MODEL
# =========================================================

model = RandomForestClassifier(

    n_estimators=250,

    random_state=42,

    class_weight="balanced",

    n_jobs=-1
)


print("Training Random Forest...")

model.fit(
    X_train,
    y_train
)


print("Model training completed.")

print()


# =========================================================
# PREDICTION
# =========================================================

predictions = model.predict(
    X_test
)


# =========================================================
# ACCURACY
# =========================================================

accuracy = accuracy_score(
    y_test,
    predictions
)


print("==============================================")
print("MODEL PERFORMANCE")
print("==============================================")

print()

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)

print()


# =========================================================
# CLASSIFICATION REPORT
# =========================================================

print("Classification Report:")
print()

print(
    classification_report(
        y_test,
        predictions
    )
)


# =========================================================
# CONFUSION MATRIX
# =========================================================

print("Confusion Matrix:")
print()

print(
    confusion_matrix(
        y_test,
        predictions
    )
)

print()


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

importance_df = pd.DataFrame({

    "Feature": features,

    "Importance":
        model.feature_importances_

})


importance_df = (
    importance_df
    .sort_values(
        by="Importance",
        ascending=False
    )
)


print("Feature Importance:")
print()


for _, row in importance_df.iterrows():

    print(
        f"{row['Feature']}: "
        f"{row['Importance'] * 100:.2f}%"
    )


print()


# =========================================================
# SAVE MODEL
# =========================================================

model_path = (
    "models/component_fault_model.pkl"
)


joblib.dump(
    model,
    model_path
)


print("==============================================")
print("MODEL SAVED")
print("==============================================")

print()

print(
    "Saved to:",
    model_path
)

print()

print("==============================================")