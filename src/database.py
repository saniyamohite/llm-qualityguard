import duckdb


def save_results(results_df, database_path="data/qualityguard.duckdb"):
    """
    Save evaluation results to DuckDB.
    """

    connection = duckdb.connect(database_path)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS llm_evaluations (
            evaluation_id INTEGER,
            question TEXT,
            expected_policy_id TEXT,
            retrieved_policy_id TEXT,
            retrieval_correct BOOLEAN,
            retrieval_similarity DOUBLE,
            actual_answer TEXT,
            score DOUBLE,
            result TEXT,
            hallucination TEXT,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.register(
        "results",
        results_df
    )

    connection.execute("""
        INSERT INTO llm_evaluations (
            evaluation_id,
            question,
            expected_policy_id,
            retrieved_policy_id,
            retrieval_correct,
            retrieval_similarity,
            actual_answer,
            score,
            result,
            hallucination,
            explanation
        )
        SELECT
            evaluation_id,
            question,
            expected_policy_id,
            retrieved_policy_id,
            retrieval_correct,
            retrieval_similarity,
            actual_answer,
            score,
            result,
            hallucination,
            explanation
        FROM results
    """)

    connection.close()