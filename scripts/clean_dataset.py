import json
import re
from tqdm import tqdm
INPUT_FILE = "data/raw_text.jsonl"
OUTPUT_FILE = "data/clean_text.jsonl"
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"[–—−]", "-", text)
    text = re.sub(r"http\S+", "", text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s\.\?\!\,\:\;\%\(\)\-]", "", text)
    if "cosine similarity" in text and "From 1 to 1" in text:
     text = text.replace("From 1 to 1", "From -1 to 1")
    return text.strip()
cleaned_count = 0
skipped_count = 0
with open(INPUT_FILE, "r", encoding="utf-8") as infile, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
    for line in tqdm(infile, desc="Cleaning Documents"):
        try:
            data = json.loads(line)
            text = clean_text(data.get("text", ""))
            if len(text.split()) < 5:
                skipped_count += 1
                continue
            cleaned_data = {
                "source": data.get("source", ""),
                "text": text
            }
            outfile.write(json.dumps(cleaned_data) + "\n")
            cleaned_count += 1
        except Exception as e:
            skipped_count += 1
            continue
print("\nCleaning Complete")
print("Cleaned Documents:", cleaned_count)
print("Skipped Documents:", skipped_count)
print("Saved to:", OUTPUT_FILE)