import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import importlib
import scripts.retrieval as retrieval
import scripts.reranker as reranker
importlib.reload(retrieval)
importlib.reload(reranker)
query = "What is FAISS?"
retrieved = retrieval.retrieve(query, k=5)
print("\n BEFORE RERANKING")
for r in retrieved:
    print("\nScore:", r["score"])
    print("Text:", r["data"]["text"][:100])
reranked = reranker.rerank(query, retrieved, top_k=3)
print("\n\n AFTER RERANKING")
for r in reranked:
    print("\nRerank Score:", r["rerank_score"])
    print("Text:", r["data"]["text"][:100])