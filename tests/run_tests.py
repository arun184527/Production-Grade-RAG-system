import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import csv
from runner import run_rag
from metrics import (
    answer_correct,
    recall_at_k,
    input_limit_test,
    grounding_score,
    hallucination_check
)
with open("tests/dataset.json", "r") as f:
    dataset = json.load(f)
results = []
total_acc = 0
total_recall = 0
total_ground = 0
latencies = []
valid_tests = 0
for item in dataset:
    query = item["query"]
    keywords = item["relevant_keywords"]
    is_valid, word_count = input_limit_test(query)
    print("\n----------------------")
    print("QUERY:", query)
    print("WORDS:", word_count)
    if not is_valid:
        print("STATUS: FAILED (Too Long)")
        continue
    result = run_rag(query)
    answer = result["answer"]
    retrieved = result["retrieved"]
    latency = result["latency"]
    acc = answer_correct(answer, keywords)
    recall = recall_at_k(retrieved, keywords)
    ground = grounding_score(answer, retrieved)
    hallucination = hallucination_check(answer, retrieved)
    total_acc += acc
    total_recall += recall
    total_ground += ground
    latencies.append(latency)
    valid_tests += 1
    print("ANSWER:", answer)
    print("ACCURACY:", round(acc, 2))
    print("RECALL:", round(recall, 2))
    print("GROUNDING:", round(ground, 2))
    print("HALLUCINATION:", "PASS" if hallucination else "FAIL")
    print("LATENCY:", round(latency, 2))
    results.append({
        "query": query,
        "answer": answer,
        "accuracy": round(acc, 2),
        "recall": round(recall, 2),
        "grounding": round(ground, 2),
        "hallucination": "PASS" if hallucination else "FAIL",
        "latency": round(latency, 2)
    })
if valid_tests > 0:
    avg_acc = total_acc / valid_tests
    avg_recall = total_recall / valid_tests
    avg_ground = total_ground / valid_tests
    avg_latency = sum(latencies) / valid_tests
    print("\n======================")
    print("FINAL REPORT")
    print("Accuracy:", round(avg_acc, 2))
    print("Recall:", round(avg_recall, 2))
    print("Grounding:", round(avg_ground, 2))
    print("Avg Latency:", round(avg_latency, 2))
from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.title = "RAG Report"
ws.append([
    "Query",
    "Accuracy",
    "Recall",
    "Grounding",
    "Hallucination",
    "Latency"
])
results.sort(key=lambda x: x["accuracy"])
for r in results:
    ws.append([
        r["query"],
        r["accuracy"],
        r["recall"],
        r["grounding"],
        r["hallucination"],
        round(r["latency"], 2)
    ])
avg_acc = round(total_acc / valid_tests, 2)
avg_recall = round(total_recall / valid_tests, 2)
avg_ground = round(total_ground / valid_tests, 2)
avg_latency = round(sum(latencies) / valid_tests, 2)
ws.append([])
ws.append([
    "FINAL SUMMARY",
    avg_acc,
    avg_recall,
    avg_ground,
    "-",
    avg_latency
])
wb.save("tests/report.xlsx")
print("Excel report saved to tests/report.xlsx")
