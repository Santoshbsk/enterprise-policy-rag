# Enterprise Policy RAG Assistant

An enterprise-style Retrieval-Augmented Generation (RAG) application for answering employee questions using company policy documents.

The application combines **semantic retrieval, cross-encoder reranking, grounding validation, scope detection, and source citations** to produce reliable and explainable answers.

Built with **Python, Google Gemini, ChromaDB, Sentence Transformers, and Streamlit**.

---

## 🚀 Project Overview

Enterprise employees frequently need quick answers to questions such as:

* How many annual leave days are available?
* How much can I claim for a domestic hotel?
* How many days can I work from home?
* What is the health insurance coverage?
* How far in advance should I submit a travel request?

Traditional keyword search can return documents that contain similar words but do not necessarily contain the most relevant information.

This project implements an enterprise RAG pipeline that:

1. Retrieves relevant policy chunks using vector similarity.
2. Reranks retrieved chunks using a cross-encoder.
3. Validates whether the question is within the assistant's scope.
4. Checks whether the retrieved context actually supports the question.
5. Generates an answer using only the retrieved policy context.
6. Provides the source policy and policy ID with the answer.
7. Safely refuses questions requiring employee-specific information.

---

# 🏗️ Architecture

```text
                         USER
                           │
                           ▼
                    User Question
                           │
                           ▼
                    Scope Detection
                           │
              ┌────────────┴────────────┐
              │                         │
          OUT OF SCOPE              IN SCOPE
              │                         │
              ▼                         ▼
       Safe Refusal              Query Embedding
                                        │
                                        ▼
                                  ChromaDB Search
                                      Top-10
                                        │
                                        ▼
                              BGE Cross-Encoder
                                   Reranking
                                        │
                                        ▼
                                  Top-3 Chunks
                                        │
                                        ▼
                                Grounding Check
                                        │
                              ┌─────────┴─────────┐
                              │                   │
                         Unsupported          Supported
                              │                   │
                              ▼                   ▼
                        Safe Response        Gemini LLM
                                                  │
                                                  ▼
                                        Answer + Citation
```

---

# 🔍 RAG Pipeline

## 1. Document Ingestion

Company policy documents are loaded and processed before being stored in the vector database.

```text
Policy Documents
       ↓
Document Loading
       ↓
Chunking
       ↓
Metadata Enrichment
       ↓
Gemini Embeddings
       ↓
ChromaDB
```

Each chunk contains metadata such as:

* Source document
* Policy type
* Policy ID
* Year
* Chunk ID

This metadata is later used for source citations.

---

## 2. Semantic Retrieval

When a user asks a question, the query is converted into an embedding and searched against the ChromaDB collection.

The system initially retrieves the **Top-10 candidates**.

---

## 3. Cross-Encoder Reranking

Vector similarity retrieval is useful for finding candidate documents, but the ranking may not always place the most relevant chunk first.

This project therefore uses:

**BAAI/bge-reranker-base**

The pipeline is:

```text
ChromaDB Top-10
       ↓
BGE Cross-Encoder
       ↓
Relevance Scoring
       ↓
Top-3 Final Context
```

The cross-encoder evaluates the question and each retrieved document together, producing a more accurate relevance ranking.

---

# 🛡️ Scope Detection

The application distinguishes between:

### In-scope questions

Questions about company policies such as:

* Leave
* Work from home
* Travel
* Employee benefits
* Insurance
* Company rules and procedures

### Out-of-scope questions

Questions requiring employee-specific information, such as:

* How many leaves did I take last month?
* What is my current leave balance?
* What is my salary?
* What is my attendance?

The application safely refuses these questions instead of attempting to retrieve unrelated policy information.

---

# 🎯 Grounding Validation

Before generating the final answer, the application checks whether the retrieved context contains enough information to answer the question.

```text
Question + Retrieved Context
            ↓
       Grounding Check
            ↓
     ┌──────┴──────┐
     │             │
SUPPORTED    NOT_SUPPORTED
     │             │
     ▼             ▼
 Gemini        Safe Response
```

If the retrieved context does not contain sufficient information, the system responds:

> I don't have enough information in the company policies to answer that.

This reduces the risk of generating unsupported answers.

---

# 📚 Source Citations

The retrieved context is enriched with source metadata before being passed to the LLM.

Example:

```text
[Source: leave_policy.txt | Policy ID: HR-LEAVE-001]

Employees are entitled to 20 days of annual leave per year.
```

The generated response provides the corresponding policy source.

Example:

```text
Answer: Employees are entitled to 20 days of annual leave per year.

Source: COMPANY LEAVE POLICY (HR-LEAVE-001)
```

This makes the response more explainable and easier to verify.

---

# 📊 Evaluation

The system was evaluated using a **20-question evaluation dataset** covering:

* Leave policies
* Travel policies
* Work-from-home policies
* Insurance
* Employee benefits

Evaluation was performed using **RAGAS**.

## Final RAGAS Results

| Metric            |      Score |
| ----------------- | ---------: |
| Context Precision | **1.0000** |
| Context Recall    | **1.0000** |
| Faithfulness      | **0.9444** |
| Answer Relevancy  | **0.8068** |

### Interpretation

**Context Precision — 1.0000**

The final retrieved context is highly relevant to the user questions.

**Context Recall — 1.0000**

The information required to answer the evaluation questions was successfully retrieved.

**Faithfulness — 0.9444**

The generated answers are strongly grounded in the retrieved policy context.

**Answer Relevancy — 0.8068**

The generated responses are generally relevant and focused on the user's questions.

---

# 📈 Retrieval Improvement

The initial retrieval pipeline used ChromaDB semantic search.

A cross-encoder reranking layer was subsequently introduced.

### Before Reranking

```text
Query
 ↓
ChromaDB Top-3
 ↓
Gemini
```

### After Reranking

```text
Query
 ↓
ChromaDB Top-10
 ↓
BGE Cross-Encoder
 ↓
Top-3
 ↓
Grounding Check
 ↓
Gemini
```

### RAGAS Comparison

| Metric            | Before Reranking | After Reranking |
| ----------------- | ---------------: | --------------: |
| Context Precision |           0.8625 |      **1.0000** |
| Context Recall    |           1.0000 |      **1.0000** |
| Faithfulness      |           0.9750 |          0.9500 |
| Answer Relevancy  |           0.7651 |      **0.8292** |

The reranking layer significantly improved context precision while maintaining perfect context recall in the evaluation.

The final application subsequently added scope detection, grounding validation, and source citations, resulting in the final evaluation scores shown above.

---

# 🧠 Key Engineering Decisions

## Why retrieve Top-10 and rerank to Top-3?

Vector search is efficient for candidate retrieval but can produce imperfect rankings.

Retrieving a larger candidate set first gives the cross-encoder more relevant candidates to evaluate.

```text
Top-10 candidate retrieval
          ↓
Cross-encoder ranking
          ↓
Top-3 high-quality context
```

This balances retrieval coverage, relevance, and LLM context size.

---

## Why use a cross-encoder?

A bi-encoder embedding model independently represents the query and documents.

A cross-encoder evaluates the query and document together:

```text
Question + Document
        ↓
Cross-Encoder
        ↓
Relevance Score
```

This generally provides stronger pairwise relevance ranking at the cost of additional inference time.

---

## Why grounding validation?

Retrieval alone does not guarantee that the retrieved documents actually answer the question.

Grounding validation provides an additional control layer:

```text
Retrieved ≠ Automatically Answerable
```

The system therefore validates the retrieved context before asking the LLM to generate the final response.

---

# 🗂️ Project Structure

```text
enterprise-policy-rag/
│
├── docs/
│   └── policy documents
│
├── evaluation/
│   ├── eval_dataset.json
│   ├── evaluate_rag.py
│   └── results/
│       └── ragas_results.csv
│
├── .env.example
├── .gitignore
├── README.md
│
├── chunking.py
├── config.py
├── embeddings.py
├── ingestion.py
├── main.py
├── rag.py
├── reranker.py
├── search.py
├── scope.py
├── grounding.py
└── requirements.txt
```

---

# ⚙️ Technology Stack

| Technology            | Purpose                    |
| --------------------- | -------------------------- |
| Python                | Application development    |
| Google Gemini         | LLM and embeddings         |
| ChromaDB              | Vector database            |
| Sentence Transformers | Cross-encoder reranking    |
| BAAI BGE Reranker     | Document relevance ranking |
| Streamlit             | Web application            |
| RAGAS                 | RAG evaluation             |
| PyTorch               | Model inference            |

---

# 🖥️ Running the Application

## 1. Clone the repository

```bash
git clone https://github.com/Santoshbsk/enterprise-policy-rag.git

cd enterprise-policy-rag
```

## 2. Create a virtual environment

```bash
python -m venv rag-env
```

Activate it on Windows:

```bash
rag-env\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file based on `.env.example`.

Example:

```text
GEMINI_API_KEY=your_api_key
EMBEDDING_MODEL=your_embedding_model
LLM_MODEL=your_llm_model
```

Do not commit your `.env` file.

## 5. Ingest the policy documents

Run the ingestion process to create the vector database.

```bash
python ingestion.py
```

## 6. Start the application

```bash
streamlit run main.py
```

The application will open in the browser.

---

# 📋 Example Questions

### Leave

```text
How many annual leave days are employees entitled to?
```

```text
How many sick leave days are available?
```

```text
How many casual leave days are available?
```

### Travel

```text
What is the domestic hotel reimbursement limit?
```

```text
How much can I claim for international hotel accommodation?
```

```text
How many days before travel should I submit a travel request?
```

### Work From Home

```text
How many days can employees work from home?
```

```text
Who approves WFH requests?
```

### Benefits

```text
What is the health insurance coverage?
```

```text
What is the life insurance coverage?
```

### Out of Scope

```text
How many leaves did I take last month?
```

```text
What is my current leave balance?
```

```text
What is my salary?
```

These questions are intentionally handled as employee-specific requests and are refused because the required information is not available in the policy knowledge base.

---

# 🔐 Security Considerations

* API keys are stored in environment variables.
* `.env` files are excluded from Git.
* Employee-specific questions are explicitly identified as out of scope.
* The LLM is instructed to use only retrieved policy context.
* Unsupported questions are rejected through grounding validation.
* Policy IDs and source metadata are preserved for traceability.

---

# ⚠️ Limitations

This project is a portfolio implementation using fictional enterprise policy documents.

Current limitations include:

* No integration with real HR systems.
* No employee authentication.
* No real employee leave balance or payroll data.
* Grounding and scope detection introduce additional LLM calls.
* Cross-encoder reranking increases retrieval latency.
* Evaluation is currently based on a 20-question dataset.
* Production deployment would require monitoring, access control, logging, and stronger evaluation coverage.

---

# 🔮 Future Improvements

Potential production enhancements include:

* Hybrid search combining semantic and keyword retrieval
* Query rewriting
* Parent-document retrieval
* Multi-query retrieval
* Evaluation using a larger benchmark dataset
* Automated citation validation
* LLM observability and tracing
* Response caching
* Enterprise authentication and authorization
* Integration with HR systems
* Agentic tool calling for employee-specific workflows
* Human escalation for unsupported requests
* Production deployment with monitoring

---

# 🎓 Learning Outcomes

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation
* Vector databases
* Embeddings
* Semantic search
* Cross-encoder reranking
* Grounded generation
* Scope classification
* Source citations
* RAG evaluation with RAGAS
* Prompt engineering
* Enterprise AI safety patterns
* Streamlit application development

---

# 👨‍💻 Author

**Santosh Bhatraju**

GenAI | Agentic AI | Conversational AI | Enterprise Automation

GitHub:
https://github.com/Santoshbsk

---

## ⭐ Project Highlights

> Enterprise-style RAG assistant with semantic retrieval, BGE cross-encoder reranking, grounding validation, scope detection, source citations, and RAGAS-based evaluation.

**Final evaluation:**

* Context Precision: **1.0000**
* Context Recall: **1.0000**
* Faithfulness: **0.9444**
* Answer Relevancy: **0.8068**
