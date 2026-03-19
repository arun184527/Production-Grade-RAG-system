import json
import re
from tqdm import tqdm
INPUT_FILE = "data/clean_text.jsonl"
OUTPUT_FILE = "data/chunks.jsonl"
def chunk_text(text, chunk_size=5, overlap=1):
    sentences = re.split(r'(?<=\?)\s+', text)
    chunks = []
    start = 0
    while start < len(sentences):
        end = start + chunk_size
        chunk = sentences[start:end]
        chunks.append(" ".join(chunk))
        start += chunk_size - overlap
    return chunks
chunk_count = 0
with open(INPUT_FILE, "r", encoding="utf-8") as infile, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
    for line in tqdm(infile, desc="Chunking Documents"):
        try:
            data = json.loads(line)
            text = data["text"]
            source = data.get("source", "")
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                chunk_data = {
                    "chunk_id": f"{source}_{i}",
                    "source": source,
                    "text": chunk
                }
                outfile.write(json.dumps(chunk_data) + "\n")
                chunk_count += 1
        except:
            continue
print("\nChunking Complete")
print("Total Chunks:", chunk_count)
print("Saved to:", OUTPUT_FILE)