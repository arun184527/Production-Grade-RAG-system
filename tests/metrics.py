def answer_correct(answer, expected):
    answer = answer.lower()
    expected = expected.lower()

    # Split expected into keywords
    keywords = expected.split()

    match_count = sum(1 for word in keywords if word in answer)

    score = match_count / len(keywords)

    return 1 if score > 0.5 else 0