import pandas as pd
import joblib
import os


# ==================================================
# LOAD AI MODELS
# ==================================================

failure_model = joblib.load(
    "models/failure_prediction_model.pkl"
)

anomaly_model_path = (
    "models/anomaly_detection_model.pkl"
)

if os.path.exists(anomaly_model_path):

    anomaly_model = joblib.load(
        anomaly_model_path
    )

else:

    anomaly_model = None


# ==================================================
# AI FEATURES
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


# ==================================================
# TEST SCENARIOS
# ==================================================

scenarios = {

    "NORMAL MACHINE": {

        "temperature": 40.0,
        "vibration": 2.0,
        "current": 7.0,
        "rpm": 1450,
        "pressure": 3.5,
        "energy_consumption": 8.0,
        "operating_hours": 1500
    },


    "WARNING MACHINE": {

        "temperature": 50.5,
        "vibration": 4.1,
        "current": 10.5,
        "rpm": 1350,
        "pressure": 4.0,
        "energy_consumption": 13.5,
        "operating_hours": 3000
    },


    "CRITICAL MACHINE": {

        "temperature": 58.0,
        "vibration": 5.5,
        "current": 12.0,
        "rpm": 1150,
        "pressure": 4.8,
        "energy_consumption": 17.0,
        "operating_hours": 4500
    }
}


# ==================================================
# TEST EACH SCENARIO
# ==================================================

print()
print("==============================================")
print("       SMART INDUSTRY AI - SCENARIO TEST")
print("==============================================")


for scenario_name, values in scenarios.items():

    # ----------------------------------------------
    # CREATE INPUT
    # ----------------------------------------------

    machine_data = pd.DataFrame(
        [values]
    )


    # ----------------------------------------------
    # FAILURE PREDICTION
    # ----------------------------------------------

    probabilities = (
        failure_model.predict_proba(
            machine_data[features]
        )[0]
    )


    failure_probability = (
        probabilities[1] * 100
    )


    # ----------------------------------------------
    # HEALTH SCORE
    # ----------------------------------------------

    health_score = (
        100 - failure_probability
    )


    health_score = max(
        0,
        min(
            100,
            health_score
        )
    )


    # ----------------------------------------------
    # RISK LEVEL
    # ----------------------------------------------

    if failure_probability >= 70:

        risk_level = "HIGH"

    elif failure_probability >= 30:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"


    # ----------------------------------------------
    # ANOMALY DETECTION
    # ----------------------------------------------

    if anomaly_model is not None:

        anomaly_result = (
            anomaly_model.predict(
                machine_data[features]
            )[0]
        )


        if anomaly_result == -1:

            anomaly_status = "ANOMALY DETECTED"

        else:

            anomaly_status = "NORMAL"

    else:

        anomaly_status = "MODEL UNAVAILABLE"


    # ----------------------------------------------
    # DISPLAY
    # ----------------------------------------------

    print()
    print("----------------------------------------------")
    print("SCENARIO:", scenario_name)
    print("----------------------------------------------")

    print(
        "Temperature:",
        values["temperature"],
        "°C"
    )

    print(
        "Vibration:",
        values["vibration"]
    )

    print(
        "Current:",
        values["current"],
        "A"
    )

    print(
        "RPM:",
        values["rpm"]
    )

    print(
        "Energy:",
        values["energy_consumption"],
        "kWh"
    )

    print()

    print(
        "Failure Probability:",
        round(
            failure_probability,
            2
        ),
        "%"
    )

    print(
        "Health Score:",
        round(
            health_score,
            2
        ),
        "/ 100"
    )

    print(
        "Risk Level:",
        risk_level
    )

    print(
        "Anomaly Status:",
        anomaly_status
    )


# ==================================================
# COMPLETE
# ==================================================

print()
print("==============================================")
print("          SCENARIO TEST COMPLETE")
print("==============================================")