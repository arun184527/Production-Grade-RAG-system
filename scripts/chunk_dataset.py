import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FOLDER = os.path.join(BASE_DIR, "../data/cleaned")
OUTPUT_FILE = os.path.join(BASE_DIR, "../data/chunks/chunks.json")

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

chunks = []
for filename in os.listdir(INPUT_FOLDER):

    if not filename.endswith(".json"):
        continue

    with open(os.path.join(INPUT_FOLDER, filename), "r", encoding="utf-8") as f:
        articles = json.load(f)

    for article in articles:

        doc_id = article["id"]
        title = article["title"]
        text = article["text"]

        words = text.split()

        start = 0
        chunk_id = 0

        while start < len(words):

            end = start + CHUNK_SIZE
            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            chunks.append({
                "doc_id": doc_id,
                "title": title,
                "chunk_id": f"{doc_id}_{chunk_id}",
                "text": chunk_text
            })

            chunk_id += 1
            start += CHUNK_SIZE - CHUNK_OVERLAP


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print("Total chunks created:", len(chunks))