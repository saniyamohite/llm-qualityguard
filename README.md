# LLM QualityGuard — Automated LLM Evaluation & Data Quality Platform

An end-to-end platform for evaluating LLM response quality, semantic retrieval, grounding, hallucination risk, and data quality using Python, SQL, RAG, automated testing, Airflow, Docker, and Power BI.

---

## Project Overview

LLM QualityGuard is a data and AI evaluation platform designed to measure the reliability and quality of Large Language Model (LLM) responses.

The project combines:

* LLM evaluation
* Semantic retrieval
* Retrieval-Augmented Generation (RAG)
* Data quality validation
* Hallucination detection
* SQL analytics
* Automated testing
* Workflow orchestration
* Dashboard-ready analytics

The system was designed around a customer-support knowledge base containing company policies and customer questions.

The goal was not simply to generate answers, but to determine whether an AI system:

1. retrieves the correct information,
2. provides a grounded answer,
3. avoids unsupported claims,
4. produces measurable quality results, and
5. can be monitored through an automated data pipeline.

---

## Architecture

```text
Customer Question
        ↓
Question / Evaluation Dataset
        ↓
Semantic Embedding
        ↓
Policy Retrieval
        ↓
Similarity Threshold
        ↓
Grounded LLM Response
        ↓
Hallucination / Faithfulness Checks
        ↓
LLM Evaluation
        ↓
SQL Evaluation Database
        ↓
Airflow Orchestration
        ↓
Power BI Analytics
```

---

## Key Results

The evaluation dataset contains:

* **475 total questions**
* **465 supported questions**
* **10 unsupported challenge questions**
* **31 policies**
* **13 categories**
* **0 duplicate questions**
* **0 questions mapped to multiple policies**

### Final Retrieval Performance

Using a similarity threshold of **0.50**:

| Metric                             |     Result |
| ---------------------------------- | ---------: |
| Supported questions                |        465 |
| Accepted supported queries         |        413 |
| Retrieval coverage                 | **88.82%** |
| Accuracy among accepted retrievals | **88.86%** |
| Unsupported questions rejected     |   **100%** |
| Unsupported false-positive rate    |     **0%** |
| Threshold rejections               |         52 |
| Wrong accepted retrievals          |         46 |

The threshold was selected to balance retrieval accuracy with protection against unsupported questions.

---

## Retrieval Evaluation

Semantic retrieval was implemented using the `all-MiniLM-L6-v2` sentence-transformer model.

The initial retrieval system achieved:

* **84.30% retrieval accuracy**
* **0.6232 average similarity**
* **15.70% retrieval error**

The evaluation exposed several difficult policy-level distinctions, particularly where policies used similar terminology.

Examples included confusion between:

* Invoice policies
* Return policies
* Warranty policies
* Shipping policies
* Payment policies

This failure analysis was used to investigate threshold behaviour and improve retrieval acceptance criteria.

---

## Threshold Analysis

Different similarity thresholds were evaluated before selecting the final threshold.

| Threshold |   Coverage | Accepted Accuracy | Unsupported FP |
| --------: | ---------: | ----------------: | -------------: |
|      0.30 |    100.00% |            84.30% |            90% |
|      0.35 |    100.00% |            84.30% |            80% |
|      0.40 |     98.49% |            85.59% |            30% |
|      0.45 |     95.48% |            86.71% |            30% |
|  **0.50** | **88.82%** |        **88.86%** |         **0%** |
|      0.55 |     77.20% |            89.42% |              — |
|      0.60 |     62.15% |            91.00% |              — |
|      0.65 |     43.66% |            92.61% |              — |
|      0.70 |     22.58% |            92.38% |              — |
|      0.75 |      7.53% |              100% |              — |

The **0.50 threshold** was selected because it eliminated unsupported false positives while retaining substantial supported-query coverage.

---

## Category-Level Performance

The final retrieval evaluation showed significant differences between policy categories.

| Category             | Coverage | Accepted Accuracy |
| -------------------- | -------: | ----------------: |
| Invoices             |     100% |            50.00% |
| Warranty             |   96.67% |            72.41% |
| Shipping             |   82.22% |            78.38% |
| Payments             |   90.00% |            85.19% |
| Orders               |   93.33% |            85.71% |
| Customer Support     |   93.33% |            89.29% |
| Refunds              |     100% |            93.33% |
| International Orders |   96.67% |              100% |
| Products             |   71.11% |              100% |
| Returns              |   53.33% |              100% |
| Subscriptions        |     100% |              100% |
| Discounts            |     100% |              100% |
| Account              |     100% |              100% |

This highlighted an important data-quality and retrieval insight:

> A single global similarity threshold does not perform equally well across every policy category.

---

## Difficulty Analysis

Questions were also evaluated by difficulty.

| Difficulty | Coverage | Accepted Accuracy |
| ---------- | -------: | ----------------: |
| Easy       |   87.10% |            89.63% |
| Medium     |   89.78% |            88.62% |
| Hard       |   89.52% |            88.29% |

The results show relatively stable retrieval performance across difficulty levels, while category-level analysis exposed much larger differences.

---

## Baseline LLM Evaluation

A Gemini model was used for baseline LLM evaluation.

Only a controlled sample of five questions was successfully evaluated because the available API free-tier quota was limited.

| Question | Score | Result |
| -------- | ----: | ------ |
| Q1       |     7 | PASS   |
| Q2       |     9 | PASS   |
| Q3       |     5 | FAIL   |
| Q4       |     1 | FAIL   |
| Q5       |    10 | PASS   |

Sample results:

* Average score: **6.4 / 10**
* PASS rate: **60%**
* FAIL rate: **40%**

This sample is intentionally reported as a controlled sample and should **not** be interpreted as statistically representative of the full evaluation dataset.

---

## RAG Implementation

The project implements a Retrieval-Augmented Generation workflow.

### Retrieval

Customer questions are converted into semantic embeddings and compared against policy embeddings using cosine similarity.

The highest-scoring policy is selected when its similarity exceeds the configured threshold.

### Grounded Generation

The RAG prompt instructs the LLM to:

* use only retrieved company policy,
* avoid unsupported information,
* provide a useful customer-facing answer,
* state when the available policy does not contain sufficient information.

This reduces the risk of the model generating answers that are not supported by the knowledge base.

---

## Hallucination Detection

A baseline lexical-overlap heuristic was implemented to identify potential hallucination risk.

The detector compares the words contained in the generated answer with the retrieved policy.

Results are classified as:

* `LOW`
* `HIGH`
* `UNKNOWN`

The current baseline uses a **50% lexical overlap threshold**.

This is intentionally treated as a baseline rather than a production hallucination detector.

### Limitations

Lexical overlap can fail when:

* the answer uses synonyms,
* the answer contains incorrect claims using policy vocabulary,
* the policy and answer have different sentence structures,
* individual claims require deeper verification.

Future versions would use semantic similarity, claim-level verification, LLM-as-a-judge evaluation, and human review.

---

## SQL Evaluation Database

Evaluation results are structured for analytical querying using DuckDB.

Example schema:

```sql
CREATE TABLE llm_evaluations (
    evaluation_id INTEGER,
    question TEXT,
    category VARCHAR,
    difficulty VARCHAR,
    expected_answer TEXT,
    actual_answer TEXT,
    retrieved_policy TEXT,
    retrieval_similarity DOUBLE,
    retrieval_correct BOOLEAN,
    score DOUBLE,
    result VARCHAR,
    hallucination VARCHAR,
    faithfulness_score DOUBLE,
    explanation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

This provides a structured foundation for:

* quality monitoring,
* retrieval analysis,
* failure investigation,
* model comparison,
* dashboard reporting.

---

## Automated Testing

Pytest tests were created for core components including:

* semantic retrieval,
* similarity score validation,
* hallucination detection,
* evaluation scoring,
* database-related functionality.

The project uses automated tests to reduce regression risk as the evaluation pipeline evolves.

---

## Airflow Orchestration

An Airflow DAG has been created to represent the automated evaluation workflow.

```text
Load Evaluation Data
        ↓
Run Retrieval
        ↓
 ┌───────────────┐
 ↓               ↓
Evaluate       Evaluate
Retrieval      Answers
 ↓               ↓
 └───────┬───────┘
         ↓
 Hallucination Check
         ↓
    Save Results
```

The DAG separates the major stages of the evaluation pipeline and provides a foundation for scheduled execution.

---

## Docker

The project includes Docker configuration to provide a reproducible Python environment.

Files included:

```text
Dockerfile
docker-compose.yml
requirements.txt
```

The container runs the QualityGuard application through:

```bash
python -m src.main
```

---

## Power BI Analytics

The project is designed to expose evaluation results for Power BI reporting.

The intended dashboard provides visibility into:

* overall retrieval coverage,
* retrieval accuracy,
* unsupported-query rejection,
* category performance,
* difficulty performance,
* threshold behaviour,
* investigation-level failures.

This allows technical evaluation results to be translated into business-readable monitoring metrics.

---

## Technology Stack

### Programming & Data

* Python
* SQL
* Pandas
* NumPy
* DuckDB

### AI / Machine Learning

* Gemini API
* Sentence Transformers
* Semantic Embeddings
* Retrieval-Augmented Generation (RAG)
* LLM Evaluation
* Hallucination Detection

### Engineering

* Pytest
* Git
* GitHub
* Docker
* Docker Compose
* Apache Airflow

### Analytics

* Power BI
* CSV-based analytical datasets

---

## Project Structure

```text
llm-qualityguard/
│
├── README.md
├── requirements.txt
├── .gitignore
├── Dockerfile
├── docker-compose.yml
│
├── data/
│   ├── knowledge_base.csv
│   └── evaluation_dataset.csv
│
├── notebooks/
│   └── LLM_QualityGuard.ipynb
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   └── retrieval.py
│   │
│   └── evaluation/
│       ├── __init__.py
│       └── evaluation.py
│
├── tests/
│   ├── test_rag.py
│   ├── test_evaluation.py
│   └── test_database.py
│
└── airflow/
    └── dags/
        └── qualityguard_pipeline.py
```

---

## Limitations

The current implementation is a portfolio-scale prototype rather than a production deployment.

Key limitations include:

* API quota prevented full LLM generation and faithfulness evaluation across all questions.
* The evaluation dataset is synthetic/programmatically generated.
* Semantic retrieval can confuse policies with similar wording.
* A single global similarity threshold is not optimal for every category.
* Hallucination detection currently uses a lexical-overlap baseline.
* LLM-as-a-judge evaluation can introduce evaluator bias.
* DuckDB is used as a lightweight prototype database.
* Airflow and Docker artifacts provide deployment foundations but are not a complete production environment.
* Power BI currently relies on prepared analytical datasets rather than a live production refresh pipeline.

These limitations are explicitly documented to distinguish demonstrated results from future production improvements.

---

## Future Improvements

Planned improvements include:

1. Hybrid retrieval combining semantic and keyword search
2. Cross-encoder reranking
3. Query rewriting
4. Metadata-aware retrieval
5. Larger human-authored evaluation datasets
6. Stronger claim-level hallucination detection
7. Structured LLM-as-a-judge evaluation
8. PostgreSQL production database
9. Production Airflow pipeline
10. Fully containerised production environment
11. Automated Power BI monitoring
12. Model comparison across multiple LLM providers
13. CI/CD and automated regression testing
14. Monitoring and retrieval/data drift detection

### Future Architecture

```text
Customer Query
        ↓
Query Understanding
        ↓
Hybrid Retrieval
        ↓
Reranking
        ↓
Grounded LLM Response
        ↓
Claim Verification
        ↓
LLM-as-a-Judge
        ↓
Quality Score
        ↓
PostgreSQL
        ↓
Airflow Monitoring
        ↓
Power BI Dashboard
```

---

## Learning Outcomes

This project provided practical experience with:

* LLM evaluation
* Data quality engineering
* Semantic search
* RAG pipelines
* Embeddings
* Similarity threshold optimisation
* SQL analytics
* Automated testing
* API integration
* Workflow orchestration
* Dockerisation
* Business intelligence
* Failure analysis
* AI system reliability

The project also demonstrates the importance of evaluating **data pipelines and AI systems together**, rather than treating LLM output quality as a purely modelling problem.

---

## Final Takeaway

LLM QualityGuard demonstrates how an AI evaluation system can be treated as a measurable data-quality problem.

Rather than only asking:

> "Did the LLM generate an answer?"

the platform asks:

> "Was the correct information retrieved, was the answer grounded in that information, can the result be measured, and can failures be monitored automatically?"

This provides a foundation for building more reliable, observable, and production-ready LLM applications.

---

## Author

**Saniya Mohite**
MSc Data Science (Distinction)

Interests:

* Data Science
* Artificial Intelligence
* LLM Evaluation
* Data Quality
* RAG
* Automation
* Analytics
* AI Reliability
