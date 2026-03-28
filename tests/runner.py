import requests
API_URL = "http://127.0.0.1:8000/chat"
def run_rag(query):
    response = requests.post(
        API_URL,
        json={"query": query},
        timeout=60
    )
    data = response.json() 
    return {
        "answer": data.get("answer", ""),
        "retrieved": data.get("retrieved_chunks", []),
        "reranked": data.get("reranked_chunks", []),
        "latency": data.get("latency", 0)
    }