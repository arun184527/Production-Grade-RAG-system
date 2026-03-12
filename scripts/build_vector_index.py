import json
import faiss
import numpy as np
embeddings = []
metadata = []
with open("embeddings/wiki_embeddings.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        embeddings.append(data["embedding"])
        metadata.append({
            "chunk_id": data["chunk_id"],
            "title": data["title"],
            "text": data["text"]
        })
embeddings = np.array(embeddings).astype("float32")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
faiss.write_index(index, "vectordb/faiss_index.bin")
with open("vectordb/metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f)
print("Vector index created successfully")