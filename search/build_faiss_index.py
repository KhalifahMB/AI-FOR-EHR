import os
import json
import glob
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
NOTES_DIR = "../data/notes"
INDEX_PATH = "./notes.index"
META_PATH = "./notes_meta.pkl"

# Load notes
def load_notes():
    notes = []
    for file in glob.glob(os.path.join(NOTES_DIR, "*.json")):
        with open(file, "r") as f:
            obj = json.load(f)
            patient_id = obj.get("patient_id", "unknown")
            note = obj.get("note", "")
            if note:
                snippet = note[:300].strip().replace("\n", " ")
                notes.append({
                    "patient_id": patient_id,
                    "snippet": snippet,
                    "full_note": note
                })
    return notes


def main():
    print("🔄 Loading notes...")
    notes = load_notes()
    texts = [n["full_note"] for n in notes]
    print(f"✅ Loaded {len(notes)} notes")

    print("🔎 Embedding with Sentence-BERT...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, convert_to_numpy=True)

    print("📦 Building FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump([{"patient_id": n["patient_id"], "snippet": n["snippet"]} for n in notes], f)

    print("✅ Index and metadata saved!")

if __name__ == "__main__":
    main()
