import pandas as pd
from sentence_transformers import SentenceTransformer

from src.rag.retrieval import (
    retrieve_top_k_policies,
    rerank_policies,
)


def main():
    print("Starting retrieval evaluation...")

    # Load data
    knowledge_base = pd.read_csv("data/knowledge_base.csv")
    evaluation_data = pd.read_csv("data/evaluation_dataset.csv")

    # Only evaluate supported questions
    supported_questions = evaluation_data[
        evaluation_data["question_type"] != "Unsupported"
    ].copy()

    print(f"Supported questions: {len(supported_questions)}")

    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Create embeddings for knowledge-base policies
    knowledge_base["embedding"] = knowledge_base["content"].apply(
        lambda x: model.encode(x)
    )

    results = []

    for _, row in supported_questions.iterrows():

        question = row["question"]
        expected_policy_id = row["policy_id"]

        # Retrieve top 3 candidates
        candidates = retrieve_top_k_policies(
            question,
            knowledge_base,
            model,
            top_k=3
        )

        # Rerank candidates
        reranked = rerank_policies(
            question,
            candidates
        )

        best_match = reranked.iloc[0]

        results.append({
            "evaluation_id": row["evaluation_id"],
            "question": question,
            "question_type": row["question_type"],
            "expected_policy_id": expected_policy_id,
            "retrieved_policy_id": best_match["policy_id"],
            "retrieval_similarity": best_match["similarity"],
            "rerank_score": best_match["rerank_score"],
            "retrieval_correct": (
                best_match["policy_id"] == expected_policy_id
            )
        })

    results_df = pd.DataFrame(results)

    # Calculate accuracy
    correct = results_df["retrieval_correct"].sum()
    total = len(results_df)
    accuracy = correct / total * 100

    print()
    print("=== Retrieval Evaluation Results ===")
    print(f"Supported questions: {total}")
    print(f"Correct reranked retrievals: {correct}")
    print(f"Reranked accuracy: {accuracy:.2f}%")
    print("Baseline accuracy: 78.92%")
    print(
        f"Improvement: {accuracy - 78.92:+.2f} percentage points"
    )

    # Save results
    results_df.to_csv(
        "data/retrieval_reranked_results.csv",
        index=False
    )

    print()
    print("Results saved to:")
    print("data/retrieval_reranked_results.csv")


if __name__ == "__main__":
    main()
