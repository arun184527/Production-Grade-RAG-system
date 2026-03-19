import os
import json
from pypdf import PdfReader
INPUT_FOLDER = "data/raw_docs"
OUTPUT_FILE = "data/raw_text.jsonl"
def read_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
def read_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
def read_json(filepath):
    texts = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                if isinstance(data, dict) and "text" in data:
                    texts.append(data["text"])
                else:
                    texts.append(str(data))
            except:
                continue
    return " ".join(texts)
def load_documents():
    files = os.listdir(INPUT_FOLDER)
    count = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for file in files:
            filepath = os.path.join(INPUT_FOLDER, file)
            ext = file.split(".")[-1].lower()
            try:
                if ext == "txt":
                    text = read_txt(filepath)
                elif ext == "pdf":
                    text = read_pdf(filepath)
                elif ext == "json":
                    text = read_json(filepath)
                else:
                    continue
                if not text or len(text.strip()) < 20:
                    continue
                data = {
                    "source": file,
                    "text": text.strip()
                }
                outfile.write(json.dumps(data) + "\n")
                count += 1
            except Exception as e:
                print(f"Error processing {file}: {e}")
    print("\nDocument Loading Complete")
    print("Total documents:", count)
    print("Saved to:", OUTPUT_FILE)
if __name__ == "__main__":
    load_documents()