# 🧠 AI-Driven Electronic Health Record (EHR) Intelligence System

This project automates clinical note analysis and builds an end-to-end AI system that extracts medical information, predicts readmission risk, and powers semantic search over patient histories — designed to simulate real hospital use.

---

## 🚀 Project Objectives

- ✅ **Automate summarization, entity extraction, and classification** from medical records.
- ✅ **Build a semantic search engine** to enable smart queries over patient history.
- ✅ **Predict 30-day readmission risk** using structured and unstructured data.
- ✅ **Deploy a user-facing Streamlit app and FastAPI backend** to simulate real-time EHR intelligence.

---

## 🧠 Methodology

### A. NLP Preprocessing
- Clean raw doctor notes
- Tokenize, remove stopwords, lemmatize
- Use `ClinicalBERT` or `spaCy` for:
  - Named Entity Recognition (NER): diseases, medications, symptoms
  - Summarization of discharge notes
  - SNOMED/ICD linking

### B. Predictive Modeling
- Combine structured Synthea data + NLP features
- Train models (XGBoost, Logistic Regression)
- Predict readmission risk or mortality

### C. Semantic Search
- Encode notes using Sentence-BERT
- Store embeddings in FAISS
- Enable natural queries (e.g., _"Find diabetic patients readmitted in last 3 months"_)

### D. Data Privacy
- Anonymize names, IDs, PHI using `spaCy` and de-identification pipelines

---

## 📦 Tech Stack

| Layer         | Tech Used                                 |
|---------------|--------------------------------------------|
| Language      | Python                                     |
| NLP           | spaCy, scispaCy, transformers (ClinicalBERT) |
| ML            | XGBoost, scikit-learn, pandas              |
| Semantic Search | Sentence-BERT, FAISS                    |
| Backend       | FastAPI                                    |
| Frontend      | Streamlit                                  |
| Database      | PostgreSQL                                 |

---

## 📁 Folder Structure

```plaintext
project_root/
├── data/
│   ├── raw/                  # Original Synthea CSVs
│   ├── notes/                # Generated clinical notes (.txt/.json)
│   └── processed/            # Cleaned dataset, NER, summaries
│
├── prediction/
│   ├── prepare_dataset.py    # Feature engineering, label creation
│   └── model_pipeline.py     # Model training, evaluation, saving
│
├── nlp/
│   ├── nlp_pipeline.py       # NER and summarization
│   └── summarizer.py         # (Optional) Note summarization
│
├── search/
│   └── faiss_index.py        # FAISS setup and query engine
│
├── api/
│   ├── main.py               # FastAPI backend entry
│   └── routers/              # Routes for NLP, prediction, search
│
├── streamlit_app/
│   └── ehr_assistant.py      # Streamlit frontend UI
│
├── database/
│   ├── schema.sql            # PostgreSQL table definitions
│   ├── load_data.py          # Load Synthea CSVs
│   └── load_notes.py         # Load generated clinical notes
│
├── requirements.txt
└── README.md
