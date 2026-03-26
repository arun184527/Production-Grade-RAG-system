import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.retrieval import retrieve
results = retrieve("What is RAG?")
for r in results:
    print("\n Score:", r["score"])
    print(" Text:", r["text"][:300])