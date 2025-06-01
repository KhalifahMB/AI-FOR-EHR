from pydantic import BaseModel
from typing import List, Optional

# ==== /predict Endpoint Schema ====


class PredictRequest(BaseModel):
    age: int
    gender: str
    race: str
    ethnicity: str
    marital_status: str
    recent_encounter_type: str
    num_encounters: int
    avg_encounter_cost: float
    num_conditions: int
    chronic_disease_flag: int
    num_medications: int
    avg_med_cost: float
    total_med_cost: float
    death_flag: int


class PredictResponse(BaseModel):
    prediction: int
    probability: float


# ==== /upload_note Endpoint Schema ====
class NoteUploadRequest(BaseModel):
    patient_id: str
    note: str


class NoteUploadResponse(BaseModel):
    message: str
    filename: str


# ==== /analyze_note (placeholder) ====
class NoteAnalysisRequest(BaseModel):
    note: str


class EntityResult(BaseModel):
    entity: str
    label: str


class NoteAnalysisResponse(BaseModel):
    entities: List[EntityResult]
    summary: Optional[str] = None


# ==== /search_notes Endpoint Schema ====
class SearchRequest(BaseModel):
    query: str


class SearchResult(BaseModel):
    patient_id: str
    snippet: str


class SearchResponse(BaseModel):
    results: List[SearchResult]
