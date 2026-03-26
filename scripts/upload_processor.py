import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
def process_uploaded_text(text, index, metadata):
    chunks = text.split(". ")
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    index.add(embeddings)
    for chunk in chunks:
        metadata.append({"text": chunk})
    return index, metadata