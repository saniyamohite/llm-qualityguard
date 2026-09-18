import re

from sklearn.metrics.pairwise import cosine_similarity


FINAL_RETRIEVAL_THRESHOLD = 0.50


def retrieve_policy(
    question,
    knowledge_base_df,
    embedding_model,
    threshold=FINAL_RETRIEVAL_THRESHOLD
):
    """
    Retrieve the most semantically similar policy for a customer question.

    Returns the best matching policy if its similarity score meets
    the configured threshold. Otherwise returns None.
    """

    question_embedding = embedding_model.encode(question)

    similarities = []

    for embedding in knowledge_base_df["embedding"]:
        similarity = cosine_similarity(
            [question_embedding],
            [embedding]
        )[0][0]

        similarities.append(similarity)

    results = knowledge_base_df.copy()
    results["similarity"] = similarities

    results = results.sort_values(
        "similarity",
        ascending=False
    )

    best_match = results.iloc[0]

    if best_match["similarity"] < threshold:
        return None

    return best_match


def retrieve_top_k_policies(
    question,
    knowledge_base_df,
    embedding_model,
    top_k=3
):
    """
    Retrieve the top-k most semantically similar policies.

    Used for retrieval analysis and future reranking.
    """

    question_embedding = embedding_model.encode(question)

    similarities = []

    for embedding in knowledge_base_df["embedding"]:
        similarity = cosine_similarity(
            [question_embedding],
            [embedding]
        )[0][0]

        similarities.append(similarity)

    results = knowledge_base_df.copy()
    results["similarity"] = similarities

    results = results.sort_values(
        "similarity",
        ascending=False
    )

    return results.head(top_k)




def check_hallucination(answer, policy):
    """
    Basic sentence-level hallucination check.

    Returns:
    LOW  -> all answer sentences have sufficient policy overlap
    HIGH -> at least one sentence has weak policy overlap
    """

    if answer is None or policy is None:
        return "UNKNOWN"

    answer_sentences = re.split(
        r"[.!?]+",
        str(answer)
    )

    policy_words = set(
        re.findall(
            r"\b[a-zA-Z]+\b",
            str(policy).lower()
        )
    )

    valid_sentences = [
        sentence.strip()
        for sentence in answer_sentences
        if sentence.strip()
    ]

    if not valid_sentences:
        return "UNKNOWN"

    for sentence in valid_sentences:

        sentence_words = set(
            re.findall(
                r"\b[a-zA-Z]+\b",
                sentence.lower()
            )
        )

        if not sentence_words:
            continue

        common_words = sentence_words.intersection(
            policy_words
        )

        overlap = len(common_words) / len(sentence_words)

        if overlap < 0.50:
            return "HIGH"

    return "LOW"


def rerank_policies(question, candidates):
    """
    Rerank retrieved policies using semantic similarity
    plus an exact title-match signal.
    """

    question_lower = question.lower()

    candidates = candidates.copy()

    candidates["title_match"] = candidates["title"].apply(
        lambda title: title.lower() in question_lower
    )

    candidates["rerank_score"] = (
        candidates["similarity"]
        + candidates["title_match"].astype(float) * 0.20
    )

    candidates = candidates.sort_values(
        "rerank_score",
        ascending=False
    )

    return candidates
