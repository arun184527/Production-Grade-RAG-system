from scripts.retrieval import search
from scripts.reranker import rerank
from scripts.prompt_builder import build_prompt
import requests
import time
def run_rag(query):
    start = time.time()
    docs = search(query, top_k=3)
    docs = rerank(query, docs, top_k=2)
    prompt = build_prompt(query, docs)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": False
        }
    )
    answer = response.json().get("response", "")
    latency = time.time() - start
    return docs, answer, latency