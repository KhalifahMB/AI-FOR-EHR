from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import predict, upload_note, patients
# , analyze_note

app = FastAPI(title="EHR AI API", version="1.0")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "API is live"}


# Include prediction route
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])

# Upload note route
app.include_router(upload_note.router,
                   prefix="/upload_note", tags=["Upload Note"])

# Patient routes
app.include_router(patients.router,
                   prefix="/patients", tags=["Get all Patient, Get Patient Summary"])


# # Analyze note route
# app.include_router(analyze_note.router,
#                    prefix="/analyze_note", tags=["Analyze Note"])
