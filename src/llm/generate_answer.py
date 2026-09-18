from google import genai
import os
import time


def generate_answer(question, policy):
    """
    Generate an answer using Gemini based only on the retrieved policy.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a customer support assistant.

Answer the customer's question using ONLY the policy provided below.

Do not invent information.
Do not add rules, dates, fees, exceptions, or details
that are not stated in the policy.

If the policy does not contain enough information to answer
the question, say that the customer should contact support.

Policy:
{policy}

Customer question:
{question}

Answer:
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text.strip()

        except Exception as error:
            if attempt == 2:
                raise

            print(
                f"Gemini request failed. "
                f"Retrying in 5 seconds... "
                f"(attempt {attempt + 1}/3)"
            )

            time.sleep(5)
