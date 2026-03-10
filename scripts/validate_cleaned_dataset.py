import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(BASE_DIR, "data", "cleaned")
total_articles = 0
short_articles = 0
for filename in os.listdir(DATA_FOLDER):
    if not filename.endswith(".json"):
        continue
    file_path = os.path.join(DATA_FOLDER, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        articles = json.load(f)
    for article in articles:
        total_articles += 1
        text = article.get("text", "")
        if len(text) < 200:
            short_articles += 1
print("Total cleaned articles:", total_articles)
print("Articles shorter than threshold:", short_articles)