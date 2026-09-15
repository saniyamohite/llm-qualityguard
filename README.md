# LLM QualityGuard

## Automated LLM Evaluation & Data Quality Platform

LLM QualityGuard is an end-to-end AI evaluation platform designed to measure the **quality, reliability, retrieval accuracy, and grounding of Large Language Model (LLM) responses**.

The project combines semantic retrieval, Retrieval-Augmented Generation (RAG), LLM evaluation, hallucination detection, SQL analytics, automated testing, workflow orchestration, Docker, and Power BI.

The goal is to move beyond simply generating an AI response and instead build a measurable framework for answering:

> **Can we trust this AI response, and can we prove why?**

---

## Project Overview

Large Language Models can generate fluent and convincing responses that may still be incorrect, incomplete, or unsupported by trusted information.

QualityGuard addresses this problem by introducing an evaluation pipeline that measures both:

### Retrieval Quality

Can the system retrieve the correct company policy for a customer question?

### Answer Quality

Does the generated LLM response correctly answer the question?

### Grounding

Is the generated answer supported by the retrieved company policy?

The platform therefore evaluates AI quality at multiple stages rather than relying on a single overall score.

---

## System Architecture

```text
                    Customer Question
                           │
                           ▼
                  Question Embedding
                           │
                           ▼
                   Semantic Retrieval
                           │
                           ▼
                  Relevant Policy
                           │
                           ▼
                    LLM / Gemini
                           │
                           ▼
                   Generated Answer
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       Answer Evaluation        Hallucination Check
              │                         │
              └────────────┬────────────┘
                           ▼
                    Quality Results
                           │
                           ▼
                      DuckDB / SQL
                           │
                           ▼
                     Power BI
```

---

## Key Results

The evaluation dataset contained:

| Metric                               |           Result |
| ------------------------------------ | ---------------: |
| Total evaluation questions           |          **475** |
| Supported questions                  |          **465** |
| Unsupported challenge questions      |           **10** |
| Company policies                     |           **31** |
| Policy categories                    |           **13** |
| Unique question texts                |          **475** |
| Final retrieval threshold            |         **0.50** |
| Supported-question coverage          |       **88.82%** |
| Accuracy when retrieval was accepted |       **88.86%** |
| Unsupported-query rejection          |         **100%** |
| Threshold rejections                 |           **52** |
| Wrong accepted retrievals            |           **46** |
| Automated tests                      | **4 / 4 passed** |

### Important interpretation

The **88.86% figure represents retrieval accuracy among accepted supported questions**.

It should not be interpreted as overall LLM answer accuracy.

The distinction is important because the project evaluates retrieval and generation as separate stages.

---

## Retrieval Evaluation

The initial semantic retrieval system achieved:

* **84.30% retrieval accuracy**
* **0.6232 average similarity**
* **15.70% retrieval error rate**

A threshold optimisation experiment was then performed.

The final operating threshold was set to:

```text
0.50
```

At this threshold:

* 88.82% of supported questions were accepted.
* 88.86% of accepted supported questions retrieved the correct policy.
* 100% of unsupported challenge questions were rejected.

This provided a practical balance between retrieval coverage, precision, and unsupported-query rejection.

---

## Retrieval Failure Analysis

The final evaluation identified **98 supported-question failures**.

These were divided into:

```text
52  Threshold Rejections
46  Wrong Accepted Retrievals
```

### Threshold Rejections

These occurred when a supported question produced a similarity score below the operating threshold.

This suggests potential improvements such as:

* query rewriting
* better policy descriptions
* improved embeddings
* metadata-aware retrieval

### Wrong Accepted Retrievals

These occurred when the retrieved policy exceeded the threshold but was still incorrect.

The largest policy confusion patterns were:

| Expected | Retrieved | Cases |
| -------- | --------- | ----: |
| INV001   | INV002    |    15 |
| SHP003   | INT002    |     8 |
| WAR001   | WAR002    |     8 |
| ORD003   | ORD001    |     4 |
| PAY001   | REF002    |     4 |

These results show that some retrieval errors are caused by **semantic overlap between closely related policies**, rather than simply low confidence.

---

## Category-Level Performance

Retrieval performance varied across categories.

Some strong categories achieved 100% accuracy when an accepted retrieval was made:

* Account
* Discounts
* Subscriptions
* International Orders
* Products
* Returns

However, Products and Returns also had lower coverage, meaning that many questions were rejected by the threshold before an incorrect retrieval could be accepted.

The weakest accepted-retrieval accuracy was observed in:

| Category | Accuracy When Accepted |
| -------- | ---------------------: |
| Invoices |             **50.00%** |
| Warranty |             **72.41%** |
| Shipping |             **78.38%** |
| Payments |             **85.19%** |
| Orders   |             **85.71%** |

This demonstrates why a single global similarity threshold cannot solve every retrieval problem.

---

## Difficulty Analysis

Retrieval performance remained relatively stable across the three difficulty levels.

| Difficulty | Coverage | Accuracy When Accepted |
| ---------- | -------: | ---------------------: |
| Easy       |   87.10% |                 89.63% |
| Medium     |   89.78% |                 88.62% |
| Hard       |   89.52% |                 88.29% |

The relatively small difference suggests that retrieval performance was influenced more by **policy overlap and question wording** than by the assigned difficulty level.

---

## Baseline LLM Evaluation

Before introducing RAG, a baseline LLM evaluation was performed.

Due to the Gemini API free-tier quota being reached during development, only a limited sample of **5 questions** could be evaluated.

The sample produced:

* **Average score: 6.4 / 10**
* **PASS rate: 60%**
* **FAIL rate: 40%**

These results are treated as a development sample rather than a statistically representative benchmark.

The baseline demonstrated that an LLM can produce fluent answers that are broader or partially inconsistent with an approved company policy.

This motivated the introduction of retrieval grounding.

---

## RAG Implementation

QualityGuard uses Retrieval-Augmented Generation to provide the LLM with trusted policy information before generating an answer.

The RAG workflow is:

```text
Customer Question
       ↓
Question Embedding
       ↓
Policy Retrieval
       ↓
Similarity Check
       ↓
Retrieved Policy
       ↓
Grounded LLM Prompt
       ↓
Generated Answer
```

The LLM is instructed to:

1. Use only the retrieved company policy.
2. Avoid unsupported assumptions.
3. Avoid using general knowledge to fill missing information.
4. State when the available policy is insufficient.
5. Provide a concise customer-facing response.

A live RAG example successfully generated a grounded answer using retrieved policy information.

Further live generation was limited by the Gemini API quota.

---

## Hallucination Detection

A lightweight hallucination-risk detector was implemented using lexical overlap between:

* the generated answer
* the retrieved policy

The detector produces:

```text
LOW
HIGH
UNKNOWN
```

A grounded answer closely matching its retrieved policy was classified as:

```text
LOW
```

This is intentionally treated as a **baseline heuristic**, rather than a definitive hallucination detector.

A production implementation would combine:

* semantic similarity
* claim-level verification
* contradiction detection
* LLM-as-a-judge
* human evaluation

---

## Automated Testing

The project uses `pytest` for deterministic regression testing.

The current test suite contains:

```text
4 tests
4 passed
0 failed
```

The tests verify:

* policy retrieval
* similarity score validity
* low hallucination risk for grounded answers
* high hallucination risk for unsupported answers

Example result:

```text
....                                                                     [100%]

4 passed in 1.58s
```

The automated tests provide regression protection for core functions.

They do not replace the larger 475-question evaluation dataset, which measures actual retrieval behaviour.

---

## SQL Analytics

DuckDB is used to store and analyse evaluation results.

The database schema includes fields for:

* evaluation ID
* question
* category
* difficulty
* expected answer
* actual answer
* retrieved policy
* retrieval similarity
* retrieval correctness
* evaluation score
* hallucination status
* faithfulness score
* explanation
* timestamp

SQL views and KPI queries were created for downstream reporting.

---

## Power BI

The project prepares analytical datasets for Power BI reporting.

The planned dashboard includes:

```text
┌─────────────────────────────────────────────────────────────┐
│                 LLM QUALITYGUARD                            │
│          Retrieval & AI Quality Monitoring                  │
├────────────┬────────────┬────────────┬─────────────────────┤
│  Coverage  │  Accepted  │  Retrieval │ Unsupported Queries │
│   88.82%   │    413     │   88.86%   │       100%          │
├────────────┴────────────┴────────────┴─────────────────────┤
│ Retrieval Accuracy by Category                             │
├──────────────────────────────┬──────────────────────────────┤
│ Retrieval Status              │ Performance by Difficulty   │
├──────────────────────────────┴──────────────────────────────┤
│ Lowest Confidence Questions                                 │
└─────────────────────────────────────────────────────────────┘
```

The dashboard is designed to help identify:

* weak policy categories
* retrieval failures
* low-confidence queries
* semantic confusion
* unsupported questions
* performance by difficulty

---

## Airflow Orchestration

An Airflow DAG was created to represent the production workflow:

```text
Load Evaluation Data
        ↓
Run Retrieval
        ↓
Evaluate Retrieval
        ↓
Evaluate Answers
        ↓
Check Hallucination
        ↓
Save Results
```

The workflow structure allows future implementation of:

* scheduled evaluation
* retries
* monitoring
* logging
* failure handling
* automated result storage

---

## Docker

Docker configuration was created to provide a reproducible application environment.

The container installs the core project dependencies and runs the QualityGuard application.

The project can therefore be extended from a notebook-based prototype into a containerised application.

---

## Technology Stack

| Technology                | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| **Python**                | Core application and data processing       |
| **Pandas**                | Dataset manipulation                       |
| **NumPy**                 | Numerical processing                       |
| **Gemini API**            | LLM generation and evaluation              |
| **Sentence Transformers** | Text embeddings                            |
| **Scikit-learn**          | Cosine similarity and retrieval evaluation |
| **DuckDB**                | SQL analytics and result storage           |
| **Pytest**                | Automated testing                          |
| **Apache Airflow**        | Workflow orchestration                     |
| **Docker**                | Reproducible deployment                    |
| **Power BI**              | Analytics and visualisation                |
| **GitHub**                | Version control and project documentation  |

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
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   └── retrieval.py
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── evaluation.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_rag.py
│   ├── test_evaluation.py
│   └── test_database.py
│
├── airflow/
│   └── dags/
│       └── qualityguard_pipeline.py
│
└── dashboard/
    ├── powerbi_dashboard_specification.md
    ├── powerbi_overall_kpis.csv
    ├── powerbi_category_performance.csv
    ├── powerbi_difficulty_performance.csv
    └── powerbi_investigation_table.csv
```

---

## Limitations

The current implementation is a prototype and has several limitations.

### LLM API Capacity

The Gemini free-tier quota was reached during development.

Consequently, full-scale LLM generation, answer evaluation, and faithfulness evaluation could not be performed across all 475 questions.

### Evaluation Dataset

The dataset was programmatically generated from the policy knowledge base.

It provides controlled benchmarking but is not equivalent to a large production dataset containing real customer conversations.

### Retrieval Model

The current retrieval system uses `all-MiniLM-L6-v2` embeddings.

A single-vector semantic search approach can struggle with closely related policies.

### Hallucination Detection

The current lexical-overlap approach is a simple baseline and cannot reliably identify every factual contradiction or unsupported claim.

### Production Infrastructure

DuckDB, Airflow, Docker, and Power BI components currently demonstrate the intended architecture rather than representing a fully deployed production environment.

---

## Future Improvements

Potential future development includes:

### Hybrid Retrieval

Combine semantic vector search with keyword-based retrieval and metadata filtering.

### Cross-Encoder Reranking

Retrieve multiple candidate policies and use a cross-encoder to select the best match.

### Query Rewriting

Transform conversational customer questions into retrieval-optimised queries.

### Metadata-Aware Retrieval

Use structured metadata such as category, intent, policy type, region, and effective date.

### Stronger Hallucination Detection

Introduce claim extraction, semantic entailment, contradiction detection, and structured verification.

### Larger Human-Authored Evaluation Dataset

Expand the benchmark with real anonymised queries, adversarial examples, ambiguous questions, and historical failure cases.

### Model Comparison

Evaluate multiple LLMs using the same benchmark to compare:

* correctness
* faithfulness
* hallucination rate
* latency
* cost

### CI/CD

Use GitHub Actions to automatically run:

* unit tests
* data validation
* retrieval regression tests
* Docker build checks

### Monitoring and Drift Detection

Monitor retrieval similarity, failure rates, hallucination rates, query patterns, and model performance over time.

---

## Key Learning Outcomes

This project provided practical experience across the full AI/data workflow:

* Designing an evaluation dataset
* Data quality validation
* Semantic embeddings
* Vector-style retrieval
* Cosine similarity
* Retrieval-Augmented Generation
* LLM-as-a-judge evaluation
* Hallucination detection
* SQL analytics
* Threshold optimisation
* Error analysis
* Automated testing
* Airflow orchestration
* Dockerisation
* Power BI reporting
* AI system limitations and evaluation methodology

---

## Final Takeaway

QualityGuard demonstrates that evaluating an AI system requires more than checking whether its responses sound convincing.

A reliable AI evaluation workflow should measure:

```text
                 ┌─────────────────┐
                 │ Retrieval       │
                 │ Quality         │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │ Answer          │
                 │ Quality         │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │ Grounding &     │
                 │ Faithfulness    │
                 └────────┬────────┘
                          ↓
                 ┌─────────────────┐
                 │ Monitoring &    │
                 │ Analytics       │
                 └─────────────────┘
```

The current project provides a reproducible baseline for this workflow, with measurable retrieval performance, automated testing, SQL analytics, orchestration, and dashboard preparation.

The long-term vision is to evolve QualityGuard into a production-grade platform for continuously benchmarking and monitoring LLM applications.

---

## Author

**Saniya Mohite**

MSc Data Science (Distinction)

Interests: Data Science · AI · LLM Evaluation · Data Quality · Automation · RAG · Analytics
