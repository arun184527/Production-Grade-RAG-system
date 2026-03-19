import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
index = faiss.read_index("vectordb/faiss.index")
with open("embeddings/metadata.json", "r") as f:
    metadata = json.load(f)
model = SentenceTransformer("all-miniLM-L6-v2")
def retrieve(query, k=3):
    query_embedding = model.encode(
        ["query: " + query],
        normalize_embeddings=True
    )
    query_embedding = np.array(query_embedding).astype("float32")
    distances, indices = index.search(query_embedding, k)
    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "score": float(distances[0][i]),
            "data": metadata[idx]
        })
    return results

def search(query, top_k=5):
    results = retrieve(query, k=top_k)
    texts = []
    for item in results:
        texts.append(item["data"]["text"])
    return texts