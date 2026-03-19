def build_prompt(query, contexts):
    # Combine all retrieved chunks
    context_text = "\n\n".join(contexts)
    prompt = f"""
You are an AI assistant.

Answer the question ONLY using the context below.
If the answer is not in the context, say "I don't know".

Context:
{context_text}

Question:
{query}

Answer:
"""
    return prompt