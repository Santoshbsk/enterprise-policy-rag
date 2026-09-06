# Enterprise Policy RAG Assistant

An enterprise-style **Retrieval-Augmented Generation (RAG)** application built with **Python, Google Gemini, ChromaDB, and Streamlit**.

The application allows users to ask questions about company policies such as Leave, Travel, Work From Home, and Employee Benefits. Relevant policy chunks are retrieved using semantic search and supplied as context to Gemini to generate grounded responses.

> **Portfolio Project:** This project uses fictional policy documents for demonstration and learning purposes. It does not connect to real employee or HR data.

---

## 🚀 Features

* 📄 Document ingestion from policy text files
* ✂️ Configurable document chunking with overlap
* 🏷️ Metadata enrichment for policy documents
* 🧠 Gemini text embeddings
* 🔎 Semantic vector search using ChromaDB
* 📚 Top-K document retrieval
* 🎯 Grounded LLM responses
* 🛡️ Explicit handling of questions that cannot be answered from policy documents
* 💬 Interactive Streamlit interface
* 🔐 Environment-based API key configuration
* ⚡ Batched embedding generation
* 📌 Retrieved source and metadata visibility

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │   Policy Documents   │
                         │                      │
                         │ Leave                │
                         │ Travel               │
                         │ WFH                  │
                         │ Benefits             │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Chunking        │
                         │                      │
                         │ Chunk Size            │
                         │ Overlap               │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Metadata       │
                         │                      │
                         │ Source               │
                         │ Policy ID            │
                         │ Department           │
                         │ Policy Type          │
                         │ Year                 │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Gemini Embeddings   │
                         │                      │
                         │ gemini-embedding-001 │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      ChromaDB        │
                         │                      │
                         │ Vector Store         │
                         │ Documents            │
                         │ Metadata             │
                         └──────────┬───────────┘
                                    │
                                    │
              ┌─────────────────────┘
              │
              ▼
      ┌──────────────────┐
      │   User Question  │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │ Query Embedding  │
      │                  │
      │ RETRIEVAL_QUERY  │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │ Semantic Search  │
      │                  │
      │ ChromaDB         │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │   Top-K Chunks   │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │ Grounding Prompt │
      │                  │
      │ Retrieved policy │
      │ context          │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │    Gemini LLM    │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │  Grounded Answer │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │    Streamlit     │
      │       UI         │
      └──────────────────┘
```

---

## 🔄 RAG Pipeline

The application follows this pipeline:

```text
Documents
    ↓
Load
    ↓
Chunk
    ↓
Add Metadata
    ↓
Generate Embeddings
    ↓
Store in ChromaDB
    ↓
User Query
    ↓
Generate Query Embedding
    ↓
Semantic Search
    ↓
Retrieve Top-K Chunks
    ↓
Build Grounding Context
    ↓
Gemini
    ↓
Grounded Answer
```

---

## 🧠 Key AI Concepts Demonstrated

### 1. Chunking

Large documents are divided into smaller pieces before embedding.

Example:

```text
Policy Document
       ↓
Chunk 1
Chunk 2
Chunk 3
Chunk 4
```

The application uses overlapping chunks to reduce the risk of splitting related information across chunk boundaries.

---

### 2. Metadata

Each chunk is associated with metadata such as:

```json
{
  "source": "leave_policy.txt",
  "department": "HR",
  "policy_type": "leave",
  "policy_id": "HR-LEAVE-001",
  "year": 2026,
  "chunk_id": 2
}
```

This allows the retrieval layer to retain the origin and classification of each piece of information.

---

### 3. Embeddings

Policy chunks are converted into numerical vectors using Google's Gemini embedding model.

The project currently uses:

```text
gemini-embedding-001
```

Google documents this model for semantic search and document retrieval and supports retrieval-specific task types including `RETRIEVAL_DOCUMENT` and `RETRIEVAL_QUERY`.

---

### 4. Semantic Search

A user's question is converted into a query embedding.

ChromaDB then performs nearest-neighbor similarity search against the stored document embeddings. Chroma supports querying with precomputed embeddings and returning the nearest results using `n_results`.

```text
User Question
      ↓
Query Embedding
      ↓
Vector Similarity Search
      ↓
Top-K Relevant Chunks
```

---

### 5. Grounding

The retrieved policy chunks are provided to Gemini as context.

The model is instructed to answer using only the retrieved information.

This helps reduce unsupported answers and hallucinations.

---

## 💡 Example Questions

### Leave Policy

```text
How many annual leave days do employees receive?
```

```text
Can unused annual leave be carried forward?
```

```text
How many days in advance should I request annual leave?
```

### Work From Home

```text
How many days can employees work from home?
```

```text
Does WFH require manager approval?
```

### Travel

```text
What is the hotel reimbursement limit for domestic travel?
```

```text
How many days before travel should I submit a request?
```

### Benefits

```text
What health insurance coverage is provided?
```

---

## 🛡️ Grounding and Hallucination Control

The application deliberately distinguishes between **company policy information** and **employee-specific information**.

For example:

```text
Question:

What is the annual leave entitlement?

Answer:

Employees receive 20 days of annual leave per year.
```

But:

```text
Question:

What is my current leave balance?

Answer:

The policy documents do not contain the employee's
individual leave balance.
```

The second question requires access to an HR/Employee Self-Service system.

This demonstrates an important enterprise AI principle:

```text
Policy Knowledge
       ↓
       RAG
       ↓
Generic policy answer


Employee-specific data
       ↓
API / Tool
       ↓
HR system
       ↓
Personalized answer
```

---

## 🖥️ Streamlit Application

The project includes a Streamlit interface for interacting with the RAG pipeline.

Run:

```bash
streamlit run main.py
```

Streamlit runs the Python application as a server and provides the interactive browser interface.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Santoshbsk/enterprise-policy-rag.git

cd enterprise-policy-rag
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv

source .venv/bin/activate
```

Using a virtual environment is recommended to isolate project dependencies.

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Gemini API key

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

Never commit `.env` or your API key to GitHub.

A template is provided as:

```text
.env.example
```

---

## 📥 Ingest Documents

Place the policy documents inside:

```text
documents/
```

Then run:

```bash
python ingest.py
```

The ingestion process:

```text
Policy Documents
      ↓
Chunking
      ↓
Metadata
      ↓
Gemini Embeddings
      ↓
ChromaDB
```

ChromaDB's persistent client stores the vector database locally so it can be reused between application runs.

---

## 🔎 Test Semantic Search

You can test retrieval independently using:

```bash
python search.py
```

This displays:

* Retrieved documents
* Metadata
* Similarity/distance information

---

## 💬 Run the RAG Application

Start Streamlit:

```bash
streamlit run main.py
```

Or:

```bash
python -m streamlit run main.py
```

Streamlit supports both approaches.

---

## 📦 Project Structure

```text
enterprise-policy-rag/
│
├── documents/
│   ├── leave_policy.txt
│   ├── travel_policy.txt
│   ├── wfh_policy.txt
│   └── benefits_policy.txt
│
├── main.py
│   └── Streamlit user interface
│
├── rag.py
│   └── RAG orchestration
│
├── ingest.py
│   └── Document ingestion pipeline
│
├── embeddings.py
│   └── Gemini embedding generation
│
├── chunking.py
│   └── Document chunking logic
│
├── config.py
│   └── Configuration and environment variables
│
├── search.py
│   └── Standalone semantic-search testing
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔐 Security

The following files/directories should not be committed:

```text
.env
.venv/
__pycache__/
chroma_db/
```

The Gemini API key should always be provided through an environment variable.

---

## 📊 Current Architecture

| Component       | Technology             |
| --------------- | ---------------------- |
| Language        | Python                 |
| LLM             | Google Gemini          |
| Embeddings      | Gemini Embedding       |
| Vector Database | ChromaDB               |
| UI              | Streamlit              |
| Retrieval       | Semantic Vector Search |
| RAG             | Custom Python pipeline |
| Configuration   | python-dotenv          |

---

## 🚧 Current Limitations

This is a portfolio/learning implementation.

* Policy documents are fictional.
* No real employee data is accessed.
* No authentication or authorization is implemented.
* ChromaDB runs locally.
* No production observability is implemented.
* No HR system integration currently exists.
* Retrieval evaluation metrics have not yet been added.

---

## 🔮 Future Enhancements

### Phase 1 — Advanced RAG

* Metadata filtering
* Similarity score thresholds
* Source citations
* Conversation history
* Query rewriting
* Reranking
* RAG evaluation
* Retrieval quality metrics

### Phase 2 — Tool Calling

Add tools such as:

```text
get_leave_balance()
get_employee_details()
check_wfh_eligibility()
get_travel_entitlement()
```

Architecture:

```text
                    User
                      │
                      ▼
                    Agent
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        RAG        HR API      Travel API
          │           │           │
          ▼           ▼           ▼
       Policies   Employee     Expenses
```

### Phase 3 — Agentic AI

The project can evolve into an enterprise HR assistant capable of:

* Retrieving policy information
* Calling enterprise APIs
* Checking employee-specific information
* Performing multi-step workflows
* Selecting tools based on user intent
* Maintaining conversation context

---

## 🎯 Learning Outcomes

This project demonstrates practical understanding of:

* Large Language Models
* Prompt Engineering
* Embeddings
* Vector Representations
* Cosine/Vector Similarity
* Semantic Search
* Document Chunking
* Metadata
* Vector Databases
* Retrieval-Augmented Generation
* Grounding
* Hallucination Mitigation
* Gemini API
* ChromaDB
* Streamlit
* Python AI Application Development

---

## 📚 References

### Google Gemini

* Google Gemini API documentation:
  https://ai.google.dev/gemini-api/docs

* Gemini Embeddings:
  https://ai.google.dev/gemini-api/docs/embeddings

* Gemini Embedding model:
  https://ai.google.dev/gemini-api/docs/models/gemini-embedding-001

Google's documentation describes embeddings as numerical representations useful for semantic search and document retrieval and documents retrieval-specific embedding task types.

### ChromaDB

* Chroma documentation:
  https://docs.trychroma.com/

* Query and Get:
  https://docs.trychroma.com/docs/querying-collections/query-and-get

* Persistent Client:
  https://docs.trychroma.com/docs/run-chroma/clients

Chroma provides nearest-neighbor vector querying and supports metadata filtering during retrieval.

### Streamlit

* Streamlit documentation:
  https://docs.streamlit.io/

* Installation:
  https://docs.streamlit.io/get-started/installation

* Create an app:
  https://docs.streamlit.io/get-started/tutorials/create-an-app

Streamlit is used here as the interactive application layer.

---

## 👨‍💻 Author

**Santosh Bhatraju**

Enterprise Automation | Conversational AI | Generative AI | RAG | Agentic AI

---

## ⭐ Project Evolution

```text
Conversational AI
       │
       ▼
      LLM
       │
       ▼
   Embeddings
       │
       ▼
 Semantic Search
       │
       ▼
      RAG
       │
       ▼
 Tool Calling
       │
       ▼
 Agentic AI
```

This project represents the transition from traditional conversational AI toward modern LLM, RAG, and Agentic AI engineering.
