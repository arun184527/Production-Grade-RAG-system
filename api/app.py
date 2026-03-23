import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI
from pydantic import BaseModel
from scripts.retrieval import search
from scripts.reranker import rerank
from scripts.prompt_builder import build_prompt
from scripts.rag_pipeline import tokenizer, model

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(request: QueryRequest):
    try:
        query = request.query
        retrieved_docs = search(query, top_k=5)
        reranked_docs = rerank(query, retrieved_docs, top_k=3)
        prompt = build_prompt(query, reranked_docs)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        token_count = inputs["input_ids"].shape[1]
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.3,
            do_sample=True
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        if "Answer:" in response:
            response = response.split("Answer:")[-1].strip()
        else:
            response = response.strip()

        if not response:
            response = "No answer generated. Try rephrasing."
        return {
            "answer": response,
            "retrieved_chunks": retrieved_docs,
            "reranked_chunks": reranked_docs,
            "token_count": int(token_count)
        }
    except Exception as e:
        return {"error": str(e)}