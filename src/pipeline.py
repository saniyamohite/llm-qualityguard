import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

from src.rag.retrieval import (
    retrieve_top_k_policies,
    rerank_policies,
)
from src.llm.generate_answer import generate_answer
from src.llm.evaluate_answer import evaluate_answer


def run_pipeline(evaluation_id):
    """
    Run the complete QualityGuard pipeline for one evaluation record.
    """

    knowledge_base = pd.read_csv("data/knowledge_base.csv")
    evaluation_data = pd.read_csv("data/evaluation_dataset.csv")

    row = evaluation_data[
        evaluation_data["evaluation_id"] == evaluation_id
    ].iloc[0]

    # Load the embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load precomputed policy embeddings
    embeddings = np.load("data/policy_embeddings.npy")

    # Attach embeddings to the knowledge base
    knowledge_base["embedding"] = list(embeddings)

    # Retrieve top candidate policies
    candidates = retrieve_top_k_policies(
        row["question"],
        knowledge_base,
        model,
        top_k=3
    )

    # Rerank the candidates
    best_policy = rerank_policies(
        row["question"],
        candidates
    ).iloc[0]

    # Generate answer using the selected policy
    actual_answer = generate_answer(
        row["question"],
        best_policy["content"]
    )

    # Evaluate the generated answer
    evaluation = evaluate_answer(
        row["question"],
        row["expected_answer"],
        actual_answer
    )

    # Return complete evaluation result
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


if __name__ == "__main__":
    result = run_pipeline(243)
    print(result)
