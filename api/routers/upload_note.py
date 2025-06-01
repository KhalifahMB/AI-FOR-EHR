from fastapi import APIRouter
from datetime import datetime
import os
import json
from ..models import NoteUploadRequest, NoteUploadResponse

router = APIRouter()

NOTES_DIR = "C:/Users/Muhammad A El-kufahn/Documents/SIWES/DATA SCIENCE ADVANCED/AI FOR EHR/data/notes"
os.makedirs(NOTES_DIR, exist_ok=True)


@router.post("/", response_model=NoteUploadResponse)
def upload_note(request: NoteUploadRequest):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{request.patient_id}_{timestamp}.json"
    filepath = os.path.join(NOTES_DIR, filename)

    note_data = {
        "patient_id": request.patient_id,
        "timestamp": timestamp,
        "note": request.note
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(note_data, f, indent=2)

    return NoteUploadResponse(
        message="Note uploaded successfully",
        filename=filename
    )
