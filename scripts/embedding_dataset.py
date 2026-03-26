import json
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import os
INPUT_FILE = "data/chunks.jsonl"
EMBEDDINGS_FILE = "embeddings/embeddings.npy"
METADATA_FILE = "embeddings/metadata.json"
os.makedirs("embeddings", exist_ok=True)
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
texts = []
metadata = []
print("Reading chunks...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in tqdm(f):
        try:
            data = json.loads(line)
            text = data["text"]
            texts.append(text)
            metadata.append({
                "chunk_id": data["chunk_id"],
                "source": data["source"],
                "text": text
            })
        except:
            continue
print(f"\nTotal chunks: {len(texts)}")
print("\nGenerating embeddings...")
embeddings = model.encode(
    texts,
    batch_size=16,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)
np.save(EMBEDDINGS_FILE, embeddings)
with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f)
print("\nEmbedding generation complete")
print("Total embeddings:", len(embeddings))
print("Embedding dimension:", embeddings.shape[1])