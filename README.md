# Enterprise Policy RAG Assistant

An enterprise-style **Retrieval-Augmented Generation (RAG)** application built with **Python, Google Gemini, ChromaDB, and Streamlit**.

The application allows users to ask questions about company policies such as **Leave, Travel, Work From Home, and Employee Benefits**. Relevant policy chunks are retrieved using semantic search and provided to Gemini as context to generate grounded responses.

> **Portfolio Project:** This project uses fictional policy documents for demonstration and learning purposes. It does not connect to real employee or HR data.

---

## 🎯 Why This Project?

This project was built to demonstrate the transition from traditional **Conversational AI and chatbot development** toward modern **Generative AI and AI Engineering**.

It provides a hands-on implementation of:

* Large Language Models
* Embeddings
* Vector databases
* Semantic search
* Document chunking
* Metadata
* Retrieval-Augmented Generation
* Grounding
* Prompt engineering
* Streamlit-based AI applications

The architecture also provides a foundation for extending the solution into **tool calling and Agentic AI**, where an AI assistant can combine policy knowledge with enterprise APIs and systems.

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
* 💾 Persistent local ChromaDB vector store

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
                    │ Chunk Size           │
                    │ Overlap              │
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
              ┌────────────────┘
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

### 1. Document Chunking

Large policy documents are divided into smaller pieces before generating embeddings.

```text
Policy Document
      ↓
   Chunk 1
   Chunk 2
   Chunk 3
   Chunk 4
```

Overlapping chunks are used to reduce the risk of separating related information across chunk boundaries.

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

Metadata allows the retrieval layer to retain the origin and classification of each piece of information.

---

### 3. Embeddings

Policy chunks are converted into numerical vectors using Google's Gemini embedding model.

The project currently uses:

```text
gemini-embedding-001
```

The model supports retrieval-specific task types including:

* `RETRIEVAL_DOCUMENT` — used when embedding documents
* `RETRIEVAL_QUERY` — used when embedding user queries

These task types are designed for document retrieval and search use cases.

---

### 4. Semantic Search

A user's question is converted into a query embedding.

ChromaDB then performs vector similarity search against the stored document embeddings and returns the most relevant chunks.

```text
User Question
      ↓
Query Embedding
      ↓
Vector Similarity Search
      ↓
Top-K Relevant Chunks
```

This allows the application to retrieve conceptually relevant information rather than relying only on exact keyword matches.

---

### 5. Grounding

The retrieved policy chunks are supplied to Gemini as context.

The model is instructed to answer using the provided policy context rather than relying on unrelated outside information.

This helps **reduce the risk of unsupported answers and hallucinations**, but does not guarantee that hallucinations are completely eliminated.

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

```text
What is the internet reimbursement limit?
```

---

## 🛡️ Grounding and Enterprise AI Boundaries

The application deliberately distinguishes between **company policy information** and **employee-specific information**.

For example:

### Policy Question

```text
Question:
How many annual leave days do employees receive?

Answer:
Employees receive 20 days of annual leave per year.
```

This type of question can be answered using the policy documents stored in the vector database.

### Employee-Specific Question

```text
Question:
What is my current leave balance?

Answer:
The policy documents do not contain the employee's
individual leave balance.
```

The second question requires access to an HR or Employee Self-Service system.

This demonstrates an important enterprise AI principle:

```text
                 Policy Knowledge
                       ↓
                      RAG
                       ↓
              Generic Policy Answer


             Employee-Specific Data
                       ↓
                    API / Tool
                       ↓
                  HR System
                       ↓
              Personalized Answer
```

This separation is important because **RAG should not be treated as a replacement for transactional enterprise systems**.

---

## 🖥️ Streamlit Application

The project includes a Streamlit interface for interacting with the RAG pipeline.

The Streamlit UI is implemented directly in `main.py`.

Run the application with:

```bash
streamlit run main.py
```

Or:

```bash
python -m streamlit run main.py
```

---

## 🛠️ Technology Stack

| Component       | Technology                              |
| --------------- | --------------------------------------- |
| Language        | Python                                  |
| LLM             | Google Gemini                           |
| Embeddings      | Gemini Embedding `gemini-embedding-001` |
| Vector Database | ChromaDB                                |
| Retrieval       | Semantic Vector Search                  |
| RAG             | Custom Python pipeline                  |
| UI              | Streamlit                               |
| Configuration   | python-dotenv                           |

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

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Santoshbsk/enterprise-policy-rag.git

cd enterprise-policy-rag
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv

.venv\Scripts\Activate.ps1
```

#### Linux/macOS

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

### 4. Configure Gemini API Key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Never commit `.env` or your API key to GitHub.

A template is provided:

```text
.env.example
```

---

## 📥 Ingest Documents

The policy documents are stored inside:

```text
documents/
```

Run the ingestion pipeline:

```bash
python ingest.py
```

The ingestion process is:

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

The application uses a persistent local ChromaDB database so that the generated vectors can be reused between application runs.

---

## 🔎 Test Semantic Search

Retrieval can also be tested independently:

```bash
python search.py
```

The search test displays:

* Retrieved documents
* Metadata
* Similarity/distance information
* Top-K retrieved chunks

---

## 💬 Run the RAG Application

Start the Streamlit application:

```bash
streamlit run main.py
```

The application allows users to:

1. Enter a natural-language policy question
2. Generate a query embedding
3. Retrieve relevant policy chunks
4. Build a grounded context
5. Send the context to Gemini
6. Display the generated answer
7. Inspect retrieved sources and metadata

---

## 🔐 Security

The following should **never** be committed to GitHub:

```text
.env
.venv/
__pycache__/
chroma_db/
```

The Gemini API key should always be provided through an environment variable.

For a production implementation, additional controls would be required, including:

* Authentication
* Authorization
* Secret management
* Access control
* Data encryption
* Audit logging
* Production observability

---

## 📊 Skills Demonstrated

This project demonstrates practical experience with:

* Python AI application development
* Generative AI
* Large Language Models
* Gemini API
* Embeddings
* Vector representations
* Semantic search
* Vector databases
* Document chunking
* Metadata enrichment
* Retrieval-Augmented Generation
* Prompt engineering
* Grounding
* Hallucination risk reduction
* ChromaDB
* Streamlit
* Enterprise AI architecture

---

## 🚧 Current Limitations

This is a **portfolio/learning implementation**, not a production HR system.

Current limitations include:

* Policy documents are fictional
* No real employee data is accessed
* No authentication or authorization
* ChromaDB runs locally
* No production observability
* No HR system integration
* No formal retrieval evaluation metrics
* No production-grade access control

These limitations are intentional so that the project remains focused on understanding and implementing the core RAG architecture.

---

## 🔮 Future Enhancements

### Phase 1 — Advanced RAG

Potential improvements include:

* Metadata filtering
* Similarity score thresholds
* Source citations
* Conversation history
* Query rewriting
* Reranking
* Retrieval evaluation
* Retrieval quality metrics
* Automated evaluation datasets

### Phase 2 — Tool Calling

The RAG system can be extended with enterprise tools such as:

```python
get_leave_balance()
get_employee_details()
check_wfh_eligibility()
get_travel_entitlement()
```

The architecture could then evolve toward:

```text
                    User
                     │
                     ▼
                   Agent
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        RAG        HR API     Travel API
          │          │          │
          ▼          ▼          ▼
      Policies    Employee   Expenses
```

### Phase 3 — Agentic AI

The application can eventually evolve into an enterprise HR assistant capable of:

* Retrieving policy information
* Selecting the appropriate knowledge source
* Calling enterprise APIs
* Checking employee-specific information
* Selecting tools based on user intent
* Performing multi-step workflows
* Maintaining conversation context
* Combining RAG with tool-based actions

---

## 🎓 Learning Outcomes

Through this project, the following concepts were implemented hands-on:

```text
LLM
 │
 ▼
Prompt Engineering
 │
 ▼
Embeddings
 │
 ▼
Vector Representation
 │
 ▼
Semantic Search
 │
 ▼
Vector Database
 │
 ▼
RAG
 │
 ▼
Grounding
 │
 ▼
Tool Calling
 │
 ▼
Agentic AI
```

The project demonstrates how a traditional conversational AI application can evolve toward modern **LLM, RAG, and Agentic AI architectures**.

---

## 📚 References

### Google Gemini

* [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs?utm_source=chatgpt.com)
* [Gemini Embeddings Documentation](https://ai.google.dev/gemini-api/docs/embeddings?utm_source=chatgpt.com)
* [Gemini Embedding Model — gemini-embedding-001](https://ai.google.dev/gemini-api/docs/models/gemini-embedding-001?utm_source=chatgpt.com)

Google's documentation describes embeddings as numerical representations useful for semantic search and document retrieval and documents retrieval-specific task types for `gemini-embedding-001`.

### ChromaDB

* [ChromaDB Documentation](https://docs.trychroma.com/?utm_source=chatgpt.com)
* [ChromaDB Querying Collections](https://docs.trychroma.com/docs/querying-collections/query-and-get?utm_source=chatgpt.com)
* [ChromaDB Clients](https://docs.trychroma.com/docs/run-chroma/clients?utm_source=chatgpt.com)

### Streamlit

* [Streamlit Documentation](https://docs.streamlit.io/?utm_source=chatgpt.com)
* [Streamlit Installation](https://docs.streamlit.io/get-started/installation?utm_source=chatgpt.com)
* [Create a Streamlit App](https://docs.streamlit.io/get-started/tutorials/create-an-app?utm_source=chatgpt.com)

---

## 👨‍💻 Author

**Santosh Bhatraju**

Enterprise Automation | Conversational AI | Generative AI | RAG | Agentic AI

---

## ⭐ Project Evolution

This project represents a progression from traditional conversational AI toward modern Generative AI engineering:

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

The goal is to progressively evolve the project from a **knowledge-grounded RAG assistant** into a **tool-enabled enterprise AI assistant**.
