import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ==================================================
# LOAD DATASET
# ==================================================

data = pd.read_csv(
    "data/industrial_dataset.csv"
)


print()
print("==============================================")
print("     SMART INDUSTRY AI - FAILURE MODEL")
print("==============================================")


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
# FEATURES
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


X = data[
    features
]


# ==================================================
# TARGET
# ==================================================

y = data[
    "failure"
]


print()
print("Failure distribution:")
print(
    y.value_counts()
)


# ==================================================
# TRAIN / TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print()
print("==============================================")
print("DATA SPLIT")
print("==============================================")

print(
    "Training readings:",
    len(X_train)
)

print(
    "Testing readings:",
    len(X_test)
)


# ==================================================
# CREATE MODEL
# ==================================================

model = RandomForestClassifier(

    n_estimators=300,

    class_weight="balanced",

    random_state=42,

    n_jobs=-1
)


# ==================================================
# TRAIN
# ==================================================

print()
print("==============================================")
print("TRAINING FAILURE MODEL")
print("==============================================")


model.fit(
    X_train,
    y_train
)


print(
    "Training completed!"
)


# ==================================================
# GET FAILURE PROBABILITIES
# ==================================================

probabilities = model.predict_proba(
    X_test
)[:, 1]


# ==================================================
# TEST MULTIPLE THRESHOLDS
# ==================================================

thresholds = [
    0.50,
    0.40,
    0.30,
    0.25,
    0.20
]


threshold_results = []


print()
print("==============================================")
print("THRESHOLD ANALYSIS")
print("==============================================")


for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)


    accuracy = accuracy_score(
        y_test,
        predictions
    )


    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )


    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )


    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )


    threshold_results.append({

        "threshold":
            threshold,

        "accuracy":
            accuracy,

        "precision":
            precision,

        "recall":
            recall,

        "f1":
            f1
    })


    print()
    print(
        "Threshold:",
        threshold
    )


    print(
        "Accuracy:",
        round(
            accuracy * 100,
            2
        ),
        "%"
    )


    print(
        "Precision:",
        round(
            precision * 100,
            2
        ),
        "%"
    )


    print(
        "Recall:",
        round(
            recall * 100,
            2
        ),
        "%"
    )


    print(
        "F1-score:",
        round(
            f1 * 100,
            2
        ),
        "%"
    )


# ==================================================
# SELECT THRESHOLD
# ==================================================
# Choose the threshold that maximizes the F1-score for optimal
# balance between false alarms and missed failures.
# ==================================================

best_result = max(
    threshold_results,
    key=lambda result: result["f1"]
)

best_threshold = best_result[
    "threshold"
]


# ==================================================
# FINAL PREDICTIONS
# ==================================================

final_predictions = (
    probabilities >= best_threshold
).astype(int)


# ==================================================
# FINAL PERFORMANCE
# ==================================================

final_accuracy = accuracy_score(
    y_test,
    final_predictions
)


final_precision = precision_score(
    y_test,
    final_predictions,
    zero_division=0
)


final_recall = recall_score(
    y_test,
    final_predictions,
    zero_division=0
)


final_f1 = f1_score(
    y_test,
    final_predictions,
    zero_division=0
)


# ==================================================
# DISPLAY FINAL MODEL
# ==================================================

print()
print("==============================================")
print("SELECTED FAILURE THRESHOLD")
print("==============================================")


print(
    "Selected threshold:",
    best_threshold
)


print()
print("Final accuracy:",
      round(
          final_accuracy * 100,
          2
      ),
      "%"
)


print(
    "Final precision:",
    round(
        final_precision * 100,
        2
    ),
    "%"
)


print(
    "Final recall:",
    round(
        final_recall * 100,
        2
    ),
    "%"
)


print(
    "Final F1-score:",
    round(
        final_f1 * 100,
        2
    ),
    "%"
)


# ==================================================
# CLASSIFICATION REPORT
# ==================================================

print()
print("==============================================")
print("CLASSIFICATION REPORT")
print("==============================================")


print(
    classification_report(
        y_test,
        final_predictions,
        zero_division=0
    )
)


# ==================================================
# CONFUSION MATRIX
# ==================================================

print()
print("==============================================")
print("CONFUSION MATRIX")
print("==============================================")


matrix = confusion_matrix(
    y_test,
    final_predictions
)


print(
    matrix
)


# ==================================================
# FEATURE IMPORTANCE
# ==================================================

print()
print("==============================================")
print("FEATURE IMPORTANCE")
print("==============================================")


importance_df = pd.DataFrame({

    "Feature":
        features,

    "Importance":
        model.feature_importances_

})


importance_df = (
    importance_df.sort_values(
        by="Importance",
        ascending=False
    )
)


for _, row in importance_df.iterrows():

    print(

        row["Feature"],

        "->",

        round(
            row["Importance"] * 100,
            2
        ),

        "%"
    )


# ==================================================
# SAVE MODEL
# ==================================================

model_path = (
    "models/failure_prediction_model.pkl"
)


joblib.dump(
    model,
    model_path
)


# Save the selected decision threshold separately
threshold_path = (
    "models/failure_threshold.pkl"
)


joblib.dump(
    best_threshold,
    threshold_path
)


print()
print("==============================================")
print("MODEL SAVING")
print("==============================================")


print(
    "Failure model saved:"
)

print(
    model_path
)


print()
print(
    "Failure threshold saved:"
)

print(
    threshold_path
)


print()
print("==============================================")
print("      FAILURE MODEL TRAINING COMPLETE")
print("==============================================")