from google import genai
import os
import json
from src.evaluation.evaluation import evaluate_score


def evaluate_answer(question, expected_answer, actual_answer):
    """
    Use Gemini as an LLM judge to evaluate an answer.

    Returns a score from 0 to 10 and a short explanation.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an evaluator for a customer support AI system.

Evaluate the actual answer against the expected answer.

Consider:
- Accuracy
- Completeness
- Relevance
- Whether the answer contradicts the expected answer
- Whether the answer invents unsupported information

Give a score from 0 to 10:

10 = completely correct and appropriate
7-9 = mostly correct with minor issues
4-6 = partially correct
1-3 = mostly incorrect
0 = completely incorrect

Return ONLY valid JSON in this exact format:

{{
    "score": 0,
    "explanation": "short explanation"
}}

Customer question:
{question}

Expected answer:
{expected_answer}

Actual answer:
{actual_answer}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    result = json.loads(response.text)

    result["result"] = evaluate_score(result["score"])

    return result