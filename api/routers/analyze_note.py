from fastapi import APIRouter
from models import NoteAnalysisRequest, NoteAnalysisResponse, EntityResult
import spacy
import re

# Initialize router and spaCy model
router = APIRouter()
nlp = spacy.load("en_core_web_sm")

# Simple medical term keywords (expand later)
medical_keywords = ["diabetes", "hypertension",
                    "asthma", "metformin", "insulin", "cough", "pain"]


@router.post("/", response_model=NoteAnalysisResponse)
def analyze_note(req: NoteAnalysisRequest):
    text = req.note
    doc = nlp(text)

    # Basic NER using keyword search (simulate ClinicalBERT)
    entities = []
    for kw in medical_keywords:
        pattern = re.compile(rf"\\b{re.escape(kw)}\\b", re.IGNORECASE)
        for match in pattern.finditer(text):
            entities.append(EntityResult(
                entity=match.group(), label="MEDICAL_TERM"))

    # Optional simple summary (simulate)
    summary = "This is a placeholder summary of the clinical note."

    return NoteAnalysisResponse(
        entities=entities,
        summary=summary
    )
