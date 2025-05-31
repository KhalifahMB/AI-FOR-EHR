import json
import os
import pandas as pd
import spacy
import string
from sqlalchemy import create_engine
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

# DB connection
DB_URI = "postgresql://postgres:Khalifah%408442@localhost:5432/ehr_system"
engine = create_engine(DB_URI)

# Load clinical notes from DB
notes_df = pd.read_sql("SELECT * FROM notes", engine)

# Load SpaCy for preprocessing
print("🔄 Loading spaCy model...")
nlp_spacy = spacy.load("en_core_web_sm", disable=["ner", "parser"])

# Load ClinicalBERT for NER (via HuggingFace)
print("🔄 Loading ClinicalBERT...")
model = AutoModelForTokenClassification.from_pretrained(
    "nlpie/distil-clinicalbert")
tokenizer = AutoTokenizer.from_pretrained("nlpie/distil-clinicalbert")
ner_pipeline = pipeline(
    "ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


# Helper function: Preprocess note text
def preprocess_text(text):
    doc = nlp_spacy(text.lower())
    tokens = [
        token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)


# Process each note
processed_results = []


def process_note(raw_text, patient_id=None):
    """
    Process a single clinical note and extract entities.
    Args:
        raw_text (str): The clinical note text.
        patient_id (str, optional): Patient identifier.
    Returns:
        dict: Processed result with patient, cleaned_text, and entities.
    """
    # Step 1: Preprocess
    cleaned_text = preprocess_text(raw_text)

    # Step 2: ClinicalBERT NER
    ner_result = ner_pipeline(cleaned_text)

    # Group by entity type
    extracted = {
        "diseases": [],
        "medications": [],
        "symptoms": [],
        "other": []
    }
    for ent in ner_result:
        label = ent["entity_group"].lower()
        text = ent["word"]
        if "disease" in label:
            extracted["diseases"].append(text)
        elif "medication" in label:
            extracted["medications"].append(text)
        elif "symptom" in label:
            extracted["symptoms"].append(text)
        else:
            extracted["other"].append(text)

    return {
        "patient": patient_id,
        "cleaned_text": cleaned_text,
        "entities": extracted
    }


# process the first 10 notes for demonstration
for index, row in notes_df.iterrows():
    if index >= 10:  # Limit to first 10 notes for demo
        break
    note_text = row["note"]
    # Assuming there's a patient_id column
    patient_id = row.get("patient_id", None)
    result = process_note(note_text, patient_id)
    processed_results.append(result)


# Save output
os.makedirs("data/processed/", exist_ok=True)

with open("data/processed/ner_results.json", "w") as f:
    json.dump(processed_results, f, indent=2)

print("✅ NLP pipeline completed. NER results saved to data/processed/ner_results.json")
