def answer_correct(answer, keywords):
    answer = answer.lower()
    matches = sum(1 for k in keywords if k in answer)
    return matches / len(keywords)
def recall_at_k(retrieved_chunks, keywords):
    text = " ".join(retrieved_chunks).lower()
    matches = sum(1 for k in keywords if k in text)
    return matches / len(keywords)
def input_limit_test(query, max_words=50):
    words = query.split()
    if len(words) > max_words:
        return False, len(words)
    return True, len(words)
def grounding_score(answer, context):
    context_text = " ".join(context).lower()
    answer = answer.lower()
    words = answer.split()
    if len(words) == 0:
        return 0
    matches = sum(1 for w in words if w in context_text)
    return matches / len(words)
def hallucination_check(answer, retrieved_chunks):
    if not retrieved_chunks:
        if "don't know" in answer.lower():
            return True
        else:
            return False
    return True