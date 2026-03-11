import json
class TextChunker:
    def __init__(self, chunk_size=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunk_count = 0
        self.article_count = 0
    def split_text(self, text):
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - self.overlap
        return chunks
    def chunk_jsonl(self, input_file, output_file):
        with open(input_file, "r", encoding="utf-8") as infile, \
             open(output_file, "w", encoding="utf-8") as outfile:
            for line in infile:
                try:
                    article = json.loads(line)
                    title = article.get("title", "")
                    text = article.get("text", "")
                    chunks = self.split_text(text)
                    for chunk in chunks:
                        chunk_data = {
                            "chunk_id": self.chunk_count,
                            "title": title,
                            "text": chunk
                        }
                        outfile.write(json.dumps(chunk_data, ensure_ascii=False) + "\n")
                        self.chunk_count += 1
                    self.article_count += 1
                    if self.article_count % 1000 == 0:
                        print("Articles processed:", self.article_count)
                except Exception:
                    continue
        print("\nChunking completed")
        print("Articles processed:", self.article_count)
        print("Total chunks created:", self.chunk_count)