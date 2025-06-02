from fastapi import APIRouter , Query
import pandas as pd
from fastapi.responses import JSONResponse

router = APIRouter()

# Load once
DATA_DIR = "C:/Users/Muhammad A El-kufahn/Documents/SIWES/DATA SCIENCE ADVANCED/AI FOR EHR/data/raw/"
patients_df = pd.read_csv(DATA_DIR + "patients.csv").fillna('')


@router.get("/all")
def get_patients(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    start = (page - 1) * limit
    end = start + limit
    total = len(patients_df)
    sliced = patients_df.iloc[start:end][[
        "Id", "FIRST", "LAST", "GENDER", "RACE", "ETHNICITY", "BIRTHDATE"]]
    return {
        "data": sliced.to_dict(orient="records"),
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/get_patient/{patient_id}")
def get_patient(patient_id: str):
    patient = patients_df[patients_df["Id"] == patient_id]
    if patient.empty:
        return JSONResponse(status_code=404, content={"error": "Patient not found"})

    return JSONResponse(status_code=200, content={
        "patient": patient.iloc[0].drop(labels=["SSN", "DRIVERS", "PASSPORT", "ZIP", "LAT", "LON"], errors="ignore").to_dict(),

    })

# f4db39b1-693d-e301-0a1f-41d26d3ced36
