import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from libraries.embedding import TextEmbedder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "wiki_chunks.jsonl")
OUTPUT_FILE = os.path.join(BASE_DIR, "embeddings", "wiki_embeddings.jsonl")
print("Starting embedding generation...\n")
embedder = TextEmbedder()
embedder.generate_embeddings(INPUT_FILE, OUTPUT_FILE)