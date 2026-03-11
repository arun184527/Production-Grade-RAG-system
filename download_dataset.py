from datasets import load_dataset
import json

print("Downloading dataset...")

dataset = load_dataset("pszemraj/simple_wikipedia", split="train")

print("Dataset downloaded")

with open("simple_wikipedia.jsonl", "w", encoding="utf-8") as f:
    for row in dataset:
        json.dump(row, f, ensure_ascii=False)
        f.write("\n")

print("Saved to simple_wikipedia.jsonl")