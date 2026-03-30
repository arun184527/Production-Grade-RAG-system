import sys
import os
import requests
import time
import faiss
import json
import re
import fitz

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.retrieval import search
from scripts.reranker import rerank
from scripts.prompt_builder import build_prompt

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


# Load index + metadata
index = faiss.read_index("vectordb/faiss.index")

with open("embeddings/metadata.json", "r") as f:
    metadata = json.load(f)


@app.post("/chat")
def chat(request: QueryRequest):
    try:
        query = request.query.strip()

        # Input limit check
        if len(query.split()) > 50:
            return {
                "answer": "Query too long. Please shorten your question.",
                "retrieved_chunks": [],
                "reranked_chunks": [],
                "input_tokens": 0,
                "output_tokens": 0,
                "latency": 0
            }

        start = time.time()

        # Retrieval
        retrieved_results = search(query, top_k=5)

        relevant_docs = [r["text"] for r in retrieved_results if r["score"] > 0.3]

        if not relevant_docs:
            return {
                "answer": "I don't know",
                "retrieved_chunks": [],
                "reranked_chunks": [],
                "input_tokens": 0,
                "output_tokens": 0,
                "latency": 0
            }

        # Reranking
        reranked = rerank(query, relevant_docs, top_k=3)

        if not reranked or len(" ".join(reranked)) < 30:
            return {
                "answer": "I don't know",
                "retrieved_chunks": relevant_docs,
                "reranked_chunks": reranked,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency": 0
            }

        # Prompt
        prompt = build_prompt(query, reranked)

        input_tokens = len(prompt.split())

        # Ollama call
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 60,
                    "temperature": 0.3
                }
            },
            timeout=60
        )

        data = response.json()

        if "response" in data:
            answer = data["response"]
        elif "message" in data:
            if isinstance(data["message"], dict):
                answer = data["message"].get("content", "")
            else:
                answer = data["message"]
        else:
            answer = str(data)

        # Clean output
        answer = answer.replace("\n", " ").strip()
        sentences = re.split(r'(?<=[.!?]) +', answer)
        answer = sentences[0] if sentences else answer

        output_tokens = len(answer.split())
        latency = time.time() - start

        return {
            "answer": answer,
            "retrieved_chunks": [r["text"] for r in retrieved_results],
            "reranked_chunks": reranked,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency": latency
        }

    except Exception as e:
        return {"error": str(e)}


# OPTIONAL: keep upload endpoint but disable processing
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    return {"message": "Upload disabled in this version"}