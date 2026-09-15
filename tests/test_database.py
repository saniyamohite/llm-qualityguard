import duckdb


def test_evaluation_database():
    connection = duckdb.connect(":memory:")

    connection.execute("""
        CREATE TABLE llm_evaluations (
            evaluation_id INTEGER,
            question TEXT,
            score DOUBLE,
            result VARCHAR
        )
    """)

    connection.execute("""
        INSERT INTO llm_evaluations
        VALUES (1, 'When will I receive my refund?', 7, 'PASS')
    """)

    result = connection.execute("""
        SELECT COUNT(*)
        FROM llm_evaluations
    """).fetchone()[0]

    assert result == 1

    connection.close()
