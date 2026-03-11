import json
import re
class DatasetCleaner:
    def __init__(self, min_length=50):
        self.min_length = min_length
        self.processed = 0
        self.skipped = 0
    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = re.sub(r"http\S+", " ", text)
        text = re.sub(r"\[\[|\]\]", "", text)
        text = re.sub(r"\n+", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    def clean_jsonl(self, input_file, output_file):
        with open(input_file, "r", encoding="utf-8") as infile, \
             open(output_file, "w", encoding="utf-8") as outfile:
            for line in infile:
                try:
                    article = json.loads(line)
                    text = article.get("text", "")
                    cleaned_text = self.clean_text(text)
                    if len(cleaned_text) < self.min_length:
                        self.skipped += 1
                        continue
                    cleaned_article = {
                        "id": article.get("id"),
                        "title": article.get("title"),
                        "text": cleaned_text
                    }
                    outfile.write(json.dumps(cleaned_article, ensure_ascii=False) + "\n")
                    self.processed += 1
                    if self.processed % 1000 == 0:
                        print("Processed:", self.processed)
                except Exception:
                    self.skipped += 1
                    continue
        print("\nCleaning finished")
        print("Total cleaned:", self.processed)
        print("Skipped:", self.skipped)