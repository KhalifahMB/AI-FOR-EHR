
import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
import os
import pickle
import joblib

class SemanticNoteSearch:
    def __init__(self, index_path="./notes.index", meta_path="./notes_meta.pkl"):
        self.index_path = index_path
        self.meta_path = meta_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        if not os.path.exists(index_path) or not os.path.exists(meta_path):
            raise ValueError("FAISS index or metadata not found.")

        self.index = faiss.read_index(index_path)
        with open(self.meta_path, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query, top_k=5):
        query_vec = self.model.encode([query])
        scores, indices = self.index.search(np.array(query_vec).astype("float32"), top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results


# Neuropathy due to type 2 diabetes
searcher = SemanticNoteSearch()

# save the searcher object and be able to use it later
joblib.dump(searcher, "searcher.joblib")
