import faiss
import json
from sentence_transformers import SentenceTransformer
class Retriever:
    def __init__(self, index_path, metadata_path):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index(index_path)
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
    def retrieve(self, query, top_k=5):
        query_vector = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)
        results = []
        for idx in indices[0]:
            results.append(self.metadata[idx])
        return results