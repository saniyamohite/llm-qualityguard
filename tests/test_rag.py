import os
import sys

os.environ["PYTHONPATH"] = os.path.abspath(".")

sys.path.insert(0, os.path.abspath("."))

from src.rag.retrieval import retrieve_policy, check_hallucination


class DummyEmbeddingModel:
    """
    Simple deterministic embedding model for testing.
    """

    def encode(self, text):
        text = text.lower()

        if "refund" in text:
            return [1.0, 0.0, 0.0]

        if "return" in text:
            return [0.9, 0.1, 0.0]

        return [0.0, 0.0, 1.0]


def test_refund_retrieval():

    knowledge_base = [
        {
            "policy_id": "REF001",
            "content": "Refunds are processed within 5 business days."
        },
        {
            "policy_id": "RET001",
            "content": "Customers can return items within 30 days."
        }
    ]

    import pandas as pd

    df = pd.DataFrame(knowledge_base)

    model = DummyEmbeddingModel()

    df["embedding"] = df["content"].apply(model.encode)

    result = retrieve_policy(
        "When will I receive my refund?",
        df,
        model
    )

    assert result is not None
    assert result["policy_id"] == "REF001"


def test_similarity_score_range():

    knowledge_base = [
        {
            "policy_id": "REF001",
            "content": "Refunds are processed within 5 business days."
        }
    ]

    import pandas as pd

    df = pd.DataFrame(knowledge_base)

    model = DummyEmbeddingModel()

    df["embedding"] = df["content"].apply(model.encode)

    result = retrieve_policy(
        "When will I receive my refund?",
        df,
        model
    )

    assert 0 <= result["similarity"] <= 1


def test_good_answer_has_low_hallucination_risk():

    policy = "Refunds are processed within 5 business days."

    answer = "Your refund is processed within 5 business days."

    result = check_hallucination(answer, policy)

    assert result == "LOW"


def test_bad_answer_has_high_hallucination_risk():

    policy = "Refunds are processed within 5 business days."

    answer = "You will receive a refund instantly in 30 seconds."

    result = check_hallucination(answer, policy)

    assert result == "HIGH"