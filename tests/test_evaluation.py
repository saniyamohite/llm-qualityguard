from src.evaluation.evaluation import (
    evaluate_score,
    calculate_evaluation_metrics,
)

import pandas as pd


def test_evaluate_score_pass():
    assert evaluate_score(7) == "PASS"


def test_evaluate_score_fail():
    assert evaluate_score(5) == "FAIL"


def test_evaluate_score_unknown():
    assert evaluate_score(None) == "UNKNOWN"


def test_calculate_evaluation_metrics():
    df = pd.DataFrame({
        "score": [7, 9, 5, 1],
        "result": ["PASS", "PASS", "FAIL", "FAIL"]
    })

    metrics = calculate_evaluation_metrics(df)

    assert metrics["average_score"] == 5.5
    assert metrics["pass_rate"] == 50.0
    assert metrics["fail_rate"] == 50.0

def test_llm_score_result():
    assert evaluate_score(10) == "PASS"
    assert evaluate_score(7) == "PASS"
    assert evaluate_score(5) == "FAIL"
    assert evaluate_score(0) == "FAIL"
