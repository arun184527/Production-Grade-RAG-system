import faiss
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
index_path = os.path.join(BASE_DIR, "vectordb", "faiss.index")
metadata_path = os.path.join(BASE_DIR, "embeddings", "metadata.json")
index = faiss.read_index(index_path)
with open(metadata_path, "r") as f:
    metadata = json.load(f)
model = SentenceTransformer("all-MiniLM-L6-v2")
def retrieve(query, k=3):
    query_embedding = model.encode([query], normalize_embeddings=True)
    query_embedding = np.array(query_embedding).astype("float32")
    distances, indices = index.search(query_embedding, k)
    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "score": float(distances[0][i]),
            "text": metadata[idx]["text"]
        })
    return results
def search(query, top_k=5):
    results = retrieve(query, k=top_k)
    return results