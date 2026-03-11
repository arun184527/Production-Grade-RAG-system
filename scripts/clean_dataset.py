import json
import os
import re
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "simple_wikipedia.jsonl")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "clean_wikipedia.jsonl")
print("Starting cleaning process...\n")
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"\[\[|\]\]", "", text)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
processed = 0
skipped = 0
with open(INPUT_FILE, "r", encoding="utf-8") as infile, \
     open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
    for line in infile:
        try:
            article = json.loads(line)
            text = article.get("text", "")
            cleaned_text = clean_text(text)
            if len(cleaned_text) < 50:
                skipped += 1
                continue
            cleaned_article = {
                "id": article.get("id"),
                "title": article.get("title"),
                "text": cleaned_text
            }
            outfile.write(json.dumps(cleaned_article, ensure_ascii=False) + "\n")
            processed += 1
            if processed % 1000 == 0:
                print("Processed:", processed)
        except Exception:
            skipped += 1
            continue
print("\nCleaning finished")
print("Total cleaned:", processed)
print("Skipped:", skipped)
print("Saved to:", OUTPUT_FILE)