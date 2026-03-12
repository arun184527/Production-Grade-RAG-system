import json
from sentence_transformers import SentenceTransformer
class TextEmbedder:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        print("Loading embedding model...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully")
    def generate_embeddings(self, input_file, output_file):
        processed = 0
        with open(input_file, "r", encoding="utf-8") as infile, \
             open(output_file, "w", encoding="utf-8") as outfile:
            for line in infile:
                try:
                    data = json.loads(line)
                    text = data.get("text", "")
                    embedding = self.model.encode(text).tolist()
                    output_data = {
                        "chunk_id": data.get("chunk_id"),
                        "title": data.get("title"),
                        "text": text,
                        "embedding": embedding
                    }
                    outfile.write(json.dumps(output_data, ensure_ascii=False) + "\n")
                    processed += 1
                    if processed % 1000 == 0:
                        print("Chunks embedded:", processed)
                except Exception:
                    continue
        print("\nEmbedding generation completed")
        print("Total chunks embedded:", processed)