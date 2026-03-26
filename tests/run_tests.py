import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from runner import run_rag
from metrics import answer_correct
with open("tests/dataset.json") as f:
    dataset = json.load(f)
results = []
for item in dataset:
    docs, answer, latency = run_rag(item["query"])
    score = answer_correct(answer, item["expected_answer"])
    results.append({
        "query": item["query"],
        "answer": answer,
        "score": score,
        "latency": latency
    })
accuracy = sum(r["score"] for r in results) / len(results)
avg_latency = sum(r["latency"] for r in results) / len(results)
print("Accuracy:", accuracy)
print("Avg Latency:", avg_latency)
print("\n----------------------")
print("QUERY:", item["query"])
print("EXPECTED:", item["expected_answer"])
print("MODEL ANSWER:", answer)
print("----------------------\n")