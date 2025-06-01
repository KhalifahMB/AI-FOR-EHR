import os
from fastapi import APIRouter
import joblib
import pandas as pd
from ..models import PredictRequest

# Define router
router = APIRouter()

# Load model and preprocessing artifacts
MODEL_PATH = "C:/Users/Muhammad A El-kufahn/Documents/SIWES/DATA SCIENCE ADVANCED/AI FOR EHR/models/model.pkl"
ENCODER_PATH = "C:/Users/Muhammad A El-kufahn/Documents/SIWES/DATA SCIENCE ADVANCED/AI FOR EHR/models/encoder.pkl"
SCALER_PATH = "C:/Users/Muhammad A El-kufahn/Documents/SIWES/DATA SCIENCE ADVANCED/AI FOR EHR/models/scaler.pkl"

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
scaler = joblib.load(SCALER_PATH)


@router.post("/")
def predict_readmission(data: PredictRequest):
    # Convert to DataFrame
    input_dict = data.dict()
    df_input = pd.DataFrame([input_dict])

    # Categorical and numeric features
    categorical = ["gender", "marital_status",
                   "race", "ethnicity", "recent_encounter_type"]
    numeric = [
        "age", "death_flag", "num_encounters", "avg_encounter_cost",
        "num_conditions", "chronic_disease_flag", "num_medications",
        "avg_med_cost", "total_med_cost"
    ]

    # Transform inputs
    encoded = encoder.transform(df_input[categorical])
    scaled = scaler.transform(df_input[numeric])

    # Combine
    X = pd.concat([
        pd.DataFrame(
            encoded, columns=encoder.get_feature_names_out(categorical)),
        pd.DataFrame(scaled, columns=numeric)
    ], axis=1)

    # Predict
    prob = model.predict_proba(X)[0][1]
    prediction = int(prob >= 0.5)

    return {
        "prediction": prediction,
        "probability": round(prob, 4)
    }
