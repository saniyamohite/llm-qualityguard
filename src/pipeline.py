import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

from src.rag.retrieval import (
    retrieve_top_k_policies,
    rerank_policies,
)
from src.llm.generate_answer import generate_answer
from src.llm.evaluate_answer import evaluate_answer


def run_pipeline(
    evaluation_id,
    knowledge_base,
    evaluation_data,
    model
):
    """
    Run the complete QualityGuard pipeline for one evaluation record.
    """

    row = evaluation_data[
        evaluation_data["evaluation_id"] == evaluation_id
    ].iloc[0]

    candidates = retrieve_top_k_policies(
        row["question"],
        knowledge_base,
        model,
        top_k=3
    )

    best_policy = rerank_policies(
        row["question"],
        candidates
    ).iloc[0]

    actual_answer = generate_answer(
        row["question"],
        best_policy["content"]
    )

    evaluation = evaluate_answer(
        row["question"],
        row["expected_answer"],
        actual_answer
    )

    return {
        "evaluation_id": row["evaluation_id"],
        "question": row["question"],
        "expected_policy_id": row["policy_id"],
        "retrieved_policy_id": best_policy["policy_id"],
        "retrieval_correct": (
            best_policy["policy_id"] == row["policy_id"]
        ),
        "retrieval_similarity": best_policy["similarity"],
        "actual_answer": actual_answer,
        "score": evaluation["score"],
        "result": evaluation["result"],
        "explanation": evaluation["explanation"],
    }


def main():
    print("Loading data...")

    knowledge_base = pd.read_csv(
        "data/knowledge_base.csv"
    )

    evaluation_data = pd.read_csv(
        "data/evaluation_dataset.csv"
    )

    print("Loading precomputed embeddings...")

    embeddings = np.load(
        "data/policy_embeddings.npy"
    )

    knowledge_base["embedding"] = list(embeddings)

    print("Loading embedding model...")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print("Running pipeline...")

    result = run_pipeline(
        evaluation_id=243,
        knowledge_base=knowledge_base,
        evaluation_data=evaluation_data,
        model=model
    )

    print(result)


if __name__ == "__main__":
    main()
