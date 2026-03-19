import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI
from pydantic import BaseModel
from scripts.rag_pipeline import generate_answer
app = FastAPI()
class QueryRequest(BaseModel):
    query: str
@app.post("/chat")
def chat(request: QueryRequest):
    answer = generate_answer(request.query)
    return {"response": answer}