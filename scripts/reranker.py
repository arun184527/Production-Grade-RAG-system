from sentence_transformers import CrossEncoder
from scripts.retrieval import search
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
def rerank(query, docs, top_k=3):
    pairs = [[query, doc] for doc in docs]
    scores = reranker.predict(pairs)
    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:top_k]]
query = "What is chunking?"
docs = search(query)
reranked_docs = rerank(query, docs)
print("Before Rerank:", docs)
print("After Rerank:", reranked_docs)