import duckdb


def main():

    connection = duckdb.connect(
        "data/qualityguard.duckdb"
    )

    results = connection.execute(
        """
        SELECT *
        FROM llm_evaluations
        """
    ).fetchdf()

    if results.empty:
        print("No evaluation results found.")
        connection.close()
        return

    average_score = results["score"].mean()

    pass_rate = (
        results["result"].eq("PASS").mean() * 100
    )

    fail_rate = (
        results["result"].eq("FAIL").mean() * 100
    )

    hallucination_rate = (
        results["hallucination"].eq("HIGH").mean() * 100
    )

    retrieval_accuracy = (
        results["retrieval_correct"].mean() * 100
    )

    print()
    print("=== QualityGuard Metrics ===")
    print(f"Evaluations: {len(results)}")
    print(f"Average score: {average_score:.2f}")
    print(f"PASS rate: {pass_rate:.2f}%")
    print(f"FAIL rate: {fail_rate:.2f}%")
    print(
        f"Hallucination rate: "
        f"{hallucination_rate:.2f}%"
    )
    print(
        f"Retrieval accuracy: "
        f"{retrieval_accuracy:.2f}%"
    )

    print()
    print("=== Results by Retrieval Status ===")

    retrieval_metrics = connection.execute(
        """
        SELECT
            retrieval_correct,
            COUNT(*) AS evaluations,
            ROUND(AVG(score), 2) AS average_score,
            ROUND(
                AVG(
                    CASE
                        WHEN result = 'PASS' THEN 1.0
                        ELSE 0.0
                    END
                ) * 100,
                2
            ) AS pass_rate
        FROM llm_evaluations
        GROUP BY retrieval_correct
        ORDER BY retrieval_correct DESC
        """
    ).fetchdf()

    print(retrieval_metrics)

    print()
    print("=== Results by Hallucination Status ===")

    hallucination_metrics = connection.execute(
        """
        SELECT
            hallucination,
            COUNT(*) AS evaluations,
            ROUND(AVG(score), 2) AS average_score,
            ROUND(
                AVG(
                    CASE
                        WHEN result = 'PASS' THEN 1.0
                        ELSE 0.0
                    END
                ) * 100,
                2
            ) AS pass_rate
        FROM llm_evaluations
        GROUP BY hallucination
        ORDER BY hallucination
        """
    ).fetchdf()

    print(hallucination_metrics)

    connection.close()


if __name__ == "__main__":
    main()