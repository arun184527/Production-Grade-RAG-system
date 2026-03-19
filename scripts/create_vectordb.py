import numpy as np
import faiss
import json
import os
EMBEDDINGS_FILE = "embeddings/embeddings.npy"
METADATA_FILE = "embeddings/metadata.json"
FAISS_INDEX_FILE = "vectordb/faiss.index"
os.makedirs("vectordb", exist_ok=True)
print("Loading embeddings...")
embeddings = np.load(EMBEDDINGS_FILE)
print("Embedding shape:", embeddings.shape)
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
print("Adding embeddings to FAISS index...")
index.add(embeddings)
faiss.write_index(index, FAISS_INDEX_FILE)
print("\nFAISS index created successfully")
print("Total vectors stored:", index.ntotal)
print("Saved to:", FAISS_INDEX_FILE)