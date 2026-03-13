import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from libraries.retriever.retriever import Retriever
retriever = Retriever(
    "vectordb/faiss_index.bin",
    "vectordb/metadata.json"
)
query = "Who invented the telephone?"
results = retriever.retrieve(query)
for r in results:
    print("\nTITLE:", r["title"])
    print("TEXT:", r["text"][:200])