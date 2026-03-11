import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from libraries.chunking import TextChunker
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "clean_wikipedia.jsonl")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "wiki_chunks.jsonl")
chunker = TextChunker(
    chunk_size=500,
    overlap=50
)
chunker.chunk_jsonl(INPUT_FILE, OUTPUT_FILE)

