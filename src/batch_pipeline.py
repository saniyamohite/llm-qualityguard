import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

from src.pipeline import run_pipeline
from src.database import save_results


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

    test_data = evaluation_data.head(5)

    results = []

    print()
    print("Running batch evaluation...")

    for evaluation_id in test_data["evaluation_id"]:

        print(f"Evaluating {evaluation_id}...")

        result = run_pipeline(
            evaluation_id=evaluation_id,
            knowledge_base=knowledge_base,
            evaluation_data=evaluation_data,
            model=model
        )

        results.append(result)

    results_df = pd.DataFrame(results)

    save_results(results_df)

    print()
    print(f"Evaluated {len(results_df)} questions.")
    print("Results saved to DuckDB.")


if __name__ == "__main__":
    main()