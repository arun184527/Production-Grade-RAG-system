import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FOLDER = os.path.join(BASE_DIR, "data", "cleaned")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "data", "chunks")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
print("Starting chunking process...\n")
total_chunks = 0
for filename in os.listdir(INPUT_FOLDER):
    if not filename.endswith(".json"):
        continue
    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    print("Processing:", filename)
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)
    chunks = []

    for article in articles:
        doc_id = article.get("id")
        title = article.get("title", "")
        text = article.get("text", "")
        words = text.split()
        start = 0
        chunk_index = 0
        while start < len(words):
            end = start + CHUNK_SIZE
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)
            chunks.append({
                "doc_id": doc_id,
                "title": title,
                "chunk_id": f"{doc_id}_{chunk_index}",
                "text": chunk_text
            })
            total_chunks += 1
            chunk_index += 1
            start += CHUNK_SIZE - CHUNK_OVERLAP

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)
    print("Chunks created:", len(chunks))
    print("Saved:", output_path, "\n")
print("Chunking completed.")
print("Total chunks created:", total_chunks)