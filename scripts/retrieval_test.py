import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.retrieval import retrieve
results = retrieve("What is FAISS?")
for r in results:
    print("\n Score:", r["score"])
    print(" Source:", r["data"]["source"])
    print(" Text:", r["data"]["text"][:200])