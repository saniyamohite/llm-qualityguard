import pandas as pd
import numpy as np
import duckdb
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

    database_path = "data/qualityguard.duckdb"

    connection = duckdb.connect(database_path)

    try:
        completed = connection.execute(
            """
            SELECT DISTINCT evaluation_id
            FROM llm_evaluations
            """
        ).fetchdf()

        completed_ids = set(
            completed["evaluation_id"].tolist()
        )

    except duckdb.CatalogException:
        completed_ids = set()

    finally:
        connection.close()

    remaining_data = evaluation_data[
        ~evaluation_data["evaluation_id"].isin(completed_ids)
    ].head(5)

    print()
    print(
        f"Already completed: {len(completed_ids)}"
    )
    print(
        f"Remaining in this batch: {len(remaining_data)}"
    )

    results = []

    for evaluation_id in remaining_data["evaluation_id"]:

        print()
        print(f"Evaluating {evaluation_id}...")

        try:
            result = run_pipeline(
                evaluation_id=evaluation_id,
                knowledge_base=knowledge_base,
                evaluation_data=evaluation_data,
                model=model
            )

            results.append(result)

            print(
                f"Completed {evaluation_id}: "
                f"{result['result']}"
            )

        except Exception as error:

            print(
                f"Skipping {evaluation_id}: {error}"
            )

    if results:

        results_df = pd.DataFrame(results)

        save_results(results_df)

        print()
        print(
            f"Saved {len(results_df)} new results to DuckDB."
        )

    else:

        print()
        print("No new results were saved.")


if __name__ == "__main__":
    main()