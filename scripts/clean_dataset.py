import os
import json
import re
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FOLDER = os.path.join(BASE_DIR, "data", "archive", "enwiki20201020")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "data", "cleaned")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"\[\d+\]", " ", text)
    text = re.sub(r"==.*?==", " ", text)
    text = re.sub(r"Category:[^\n]+", " ", text)
    text = re.sub(r"\{\{[\s\S]*?\}\}", " ", text)
    text = re.sub(r"\{\|[\s\S]*?\|\}", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"^\*\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\|-|\||!", " ", text)
    text = re.sub(r"__.*?__", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
print("\nStarting cleaning process...\n")
total_articles = 0
total_cleaned = 0
for filename in os.listdir(INPUT_FOLDER):
    if not filename.endswith(".json"):
        continue
    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    print("Processing:", filename)
    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)
    print("Articles found:", len(articles))
    cleaned_articles = []
    for article in articles:
        total_articles += 1
        article_id = article.get("id")
        title = article.get("title", "")
        text = article.get("text", "")
        cleaned = clean_text(text)

        if len(cleaned) < 200:
            continue
        cleaned_articles.append({
            "id": article_id,
            "title": title,
            "text": cleaned
        })
        total_cleaned += 1
    print("Cleaned articles:", len(cleaned_articles))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_articles, f, indent=2)
    print("Saved cleaned file\n")

print("\nCleaning completed.")
print("Total articles processed:", total_articles)
print("Total cleaned articles:", total_cleaned)