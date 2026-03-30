import numpy as np
import faiss
import re
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def clean_text(text):
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_text(text):
    text = clean_text(text)

    sentences = text.split(".")
    chunks = []

    for s in sentences:
        s = s.strip()

        if len(s) > 20:
            chunks.append(s)

    
    if not chunks:
        chunks = [text]

    return chunks


def create_index_from_text(text):
    chunks = chunk_text(text)

    print("\n[DEBUG CHUNKS]:", chunks)

    embeddings = model.encode(chunks, normalize_embeddings=True)
    embeddings = np.array(embeddings).astype("float32")

    if len(embeddings.shape) == 1:
        embeddings = embeddings.reshape(1, -1)

    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    metadata = [{"text": c} for c in chunks]

    return index, metadata