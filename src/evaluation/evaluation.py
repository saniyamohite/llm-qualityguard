def evaluate_score(score):
    """
    Convert a numerical LLM evaluation score into PASS or FAIL.
    """

    if score is None:
        return "UNKNOWN"

    if score >= 7:
        return "PASS"

    return "FAIL"


def calculate_evaluation_metrics(results_df):
    """
    Calculate basic evaluation metrics from an evaluation DataFrame.
    """

    evaluated = results_df.dropna(subset=["score"])

    if len(evaluated) == 0:
        return {
            "average_score": None,
            "pass_rate": None,
            "fail_rate": None
        }

    average_score = evaluated["score"].mean()

    pass_rate = (
        evaluated["result"].eq("PASS").mean() * 100
    )

    fail_rate = (
        evaluated["result"].eq("FAIL").mean() * 100
    )

    return {
        "average_score": average_score,
        "pass_rate": pass_rate,
        "fail_rate": fail_rate
    }