# LLM QualityGuard

Automated LLM evaluation and data-quality platform for testing customer-support AI systems.

## Overview

LLM QualityGuard evaluates whether an AI-generated customer-support answer is accurate, relevant, complete, and grounded in the underlying company policy.

The platform combines semantic retrieval, reranking, LLM-based evaluation, hallucination detection, SQL storage, and automated metrics.

## Architecture

Customer Question
        ↓
Semantic Retrieval
        ↓
Policy Reranking
        ↓
LLM Answer Generation
        ↓
LLM-as-a-Judge
        ↓
Hallucination Check
        ↓
DuckDB
        ↓
Evaluation Metrics

## Key Features

- Semantic policy retrieval using Sentence Transformers
- Top-k retrieval with transparent reranking
- Exact-title matching signal for ambiguous queries
- Gemini-based answer generation
- Gemini LLM-as-a-Judge scoring from 0–10
- PASS/FAIL classification
- Sentence-level hallucination detection
- DuckDB evaluation storage
- Batch evaluation pipeline
- SQL-based evaluation metrics
- API retry and quota-aware error handling
- Automated pytest test suite
- Docker and Airflow-ready project structure

## Dataset

The evaluation dataset contains:

- 31 policies
- 475 customer questions
- 465 supported questions
- 10 unsupported challenge questions
- 14 categories
- Multiple question types and difficulty levels

## Retrieval Evaluation

Initial semantic retrieval accuracy:

**78.92%**

After transparent reranking:

**99.35%**

The reranking layer improved retrieval by **20.43 percentage points**, correcting 43 of the original 46 retrieval errors in the evaluation dataset.

## Example End-to-End Result

For a return-window question:

- Retrieved policy: `RET001`
- Retrieval: Correct
- Generated answer: Correct
- LLM judge score: `10/10`
- Result: `PASS`
- Hallucination: `LOW`

## Testing

```bash
py -m pytest -q