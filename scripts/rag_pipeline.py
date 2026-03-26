import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.retrieval import search
from scripts.reranker import rerank
from scripts.prompt_builder import build_prompt
def generate_answer(query):
    try:
        docs = search(query, top_k=3)
        docs = rerank(query, docs, top_k=2)
        prompt = build_prompt(query, docs)
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",  
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 120,
                    "temperature": 0.7
                }
            },
            timeout=60
        )
        result = response.json()["response"].strip()
        return result
    except Exception as e:
        return f"Error: {str(e)}"
if __name__ == "__main__":
    while True:
        query = input("\nEnter your question (or type 'exit'): ")
        if query.lower() == "exit":
            break

        answer = generate_answer(query)
        print("\nAnswer:\n", answer)