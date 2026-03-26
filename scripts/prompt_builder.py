def build_prompt(query, contexts):
    context_text = "\n\n".join(contexts)

    return f"""
Context:
{context_text}

Question: {query}

Answer:
"""