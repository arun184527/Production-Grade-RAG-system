import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "clean_wikipedia.jsonl")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "wiki_chunks.jsonl")
print("Starting chunking process...\n")
CHUNK_SIZE = 500   
CHUNK_OVERLAP = 50
def split_text(text):
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - CHUNK_OVERLAP
    return chunks
chunk_id = 0
articles_processed = 0
with open(INPUT_FILE, "r", encoding="utf-8") as infile, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
    for line in infile:
        try:
            article = json.loads(line)
            title = article.get("title", "")
            text = article.get("text", "")
            chunks = split_text(text)
            for chunk in chunks:
                chunk_data = {
                    "chunk_id": chunk_id,
                    "title": title,
                    "text": chunk
                }
                outfile.write(json.dumps(chunk_data, ensure_ascii=False) + "\n")
                chunk_id += 1
            articles_processed += 1
            if articles_processed % 1000 == 0:
                print("Articles processed:", articles_processed)
        except Exception:
            continue
print("\nChunking completed")
print("Total articles processed:", articles_processed)
print("Total chunks created:", chunk_id)
print("Saved to:", OUTPUT_FILE)