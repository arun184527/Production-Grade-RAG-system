import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.rag_pipeline import generate_answer_with_sources
query = "What are Embeddings?"
answer, sources = generate_answer_with_sources(query)
print("\n Question:", query)
print("\n Answer:\n", answer)
print("\n Sources:")
for s in sources:
    print("-", s["data"]["text"][:100])