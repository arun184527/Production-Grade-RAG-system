from sentence_transformers import CrossEncoder
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
def rerank(query, docs, top_k=3, score_threshold=0.3):
    if not docs:
        return []
    try:
        pairs = [[query, doc] for doc in docs]
        scores = reranker.predict(pairs)
        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )
        filtered = [doc for doc, score in ranked if score > score_threshold]
        if not filtered:
            return []
        return filtered[:top_k]
    except Exception as e:
        print("Reranker error:", e)
        return docs[:top_k]  