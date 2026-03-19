import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.retrieval import retrieve
from scripts.reranker import rerank
from scripts.prompt_builder import build_prompt
query = "What is FAISS?"
retrieved = retrieve(query, k=5)
reranked = rerank(query, retrieved, top_k=3)
context = "\n\n".join([f"Chunk:\n{r['data']['text']}" for r in reranked])
prompt = build_prompt(query, context)
print("\n FINAL PROMPT:\n")
print(prompt)