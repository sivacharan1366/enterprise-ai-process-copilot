# 🤖 Enterprise AI Process Copilot

An AI-powered enterprise assistant that combines **Retrieval-Augmented Generation (RAG)** with **business process automation**.

The system can answer questions using internal enterprise policy documents and automate an IT equipment request workflow from employee submission through manager approval, IT processing, and completion.

---

## 🚀 Overview

Enterprise employees often need quick answers about company policies and procedures, while operational requests still require multiple manual steps.

This project combines both capabilities into a single application.

### 🧠 Enterprise Knowledge Assistant

- Loads internal TXT/PDF documents
- Splits documents into meaningful sections
- Generates semantic embeddings
- Stores embeddings in a vector database
- Retrieves relevant policy information
- Uses an LLM to generate grounded answers
- Displays the sources used for each answer

### ⚙️ Process Automation

The application also supports an IT laptop-request workflow:

```text
Employee Request
       ↓
Pending Manager Approval
       ↓
   ┌───┴────┐
   ↓        ↓
Approved   Rejected
   ↓
IT Processing
   ↓
Completed
```

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      Streamlit      │
                    │      Web UI         │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │   RAG Assistant  │        │ Workflow Engine  │
       └────────┬─────────┘        └────────┬─────────┘
                │                           │
                ▼                           ▼
       ┌──────────────────┐        ┌──────────────────┐
       │ Knowledge Base   │        │ Laptop Requests  │
       │ TXT / PDF        │        │ JSON Storage     │
       └────────┬─────────┘        └──────────────────┘
                │
                ▼
       ┌──────────────────┐
       │ Document Chunks  │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ OpenRouter       │
       │ Embeddings API   │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ ChromaDB         │
       │ Vector Store     │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ Semantic Search  │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ OpenRouter LLM   │
       │ GPT-OSS-20B      │
       └────────┬─────────┘
                │
                ▼
       Grounded Answer
       + Source Attribution
```

---

## 🔄 RAG Pipeline

The knowledge assistant follows a Retrieval-Augmented Generation pipeline.

### 1. Document ingestion

Enterprise policy documents are stored in:

```text
data/
└── knowledge_base/
    └── IT_Equipment_Policy.txt
```

The application also supports PDF documents.

### 2. Document processing

Documents are extracted and divided into meaningful chunks.

The current implementation uses paragraph-aware chunking to avoid cutting policy sections in the middle of sentences.

### 3. Embedding generation

Each chunk is converted into a numerical vector using the OpenRouter embeddings API.

### 4. Vector storage

Embeddings are stored and searched using ChromaDB.

### 5. Semantic retrieval

When a user asks a question, the application retrieves the most relevant enterprise knowledge chunks.

### 6. LLM generation

The retrieved context is provided to the LLM through a controlled prompt.

The assistant is instructed to:

- Use only the provided enterprise context
- Avoid unsupported assumptions
- Avoid inventing company policies
- State when the knowledge base does not contain an answer
- Cite relevant sources

### 7. Source attribution

The application displays the source document and similarity score alongside the generated response.

---

## ⚙️ Enterprise Workflow

The application currently supports an IT laptop request process.

### Employee Request

An employee provides:

- Employee name
- Department
- Reason for request
- Required specifications

A unique request ID is generated.

Example:

```text
IT-0001
```

### Manager Approval

Requests initially enter:

```text
Pending Manager Approval
```

Managers can:

```text
Approve
Reject
```

### IT Processing

Approved requests move to:

```text
IT Processing
```

### Completion

After IT processing, the request can be marked:

```text
Completed
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web interface |
| OpenRouter | Embeddings and LLM API |
| GPT-OSS-20B | Response generation |
| ChromaDB | Vector storage and retrieval |
| PyPDF | PDF document extraction |
| Requests | API communication |
| python-dotenv | Environment configuration |
| JSON | Local workflow persistence |

---

## 📁 Project Structure

```text
enterprise-ai-process-copilot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── data/
│   └── knowledge_base/
│       └── IT_Equipment_Policy.txt
│
└── src/
    ├── llm.py
    ├── rag.py
    └── workflow.py
```

Generated files such as request data, vector stores, environment variables, and virtual environments are excluded from version control.

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Never commit your real API key to GitHub.

---

## ▶️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sivacharan1366/enterprise-ai-process-copilot.git
cd enterprise-ai-process-copilot
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the API key

Create `.env`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 5. Run the application

```powershell
python -m streamlit run app.py
```

The application will open in your browser.

---

## 💬 Example Knowledge Query

Example question:

```text
Who needs to approve a laptop request?
```

The system retrieves the relevant section of the IT Equipment Policy and generates a grounded response.

Example answer:

```text
The laptop request must be approved by the employee's
reporting manager. Requests for high-performance
workstations may require additional approval from
the IT department.
```

The corresponding source document is displayed in the application.

---

## 📋 Example Process

A user can create a laptop request:

```text
Employee:
John Doe

Department:
Engineering

Reason:
Current laptop is outdated

Specifications:
16GB RAM, 512GB SSD
```

The system generates:

```text
Request ID: IT-0001
Status: Pending Manager Approval
```

The request can then progress through the enterprise workflow:

```text
Pending Manager Approval
          ↓
       Approved
          ↓
    IT Processing
          ↓
       Completed
```

---

## 📸 Application Screenshots

The application includes:

- Enterprise knowledge assistant
- RAG responses with source attribution
- Laptop request creation
- Manager approval interface
- IT processing workflow
- Completed request tracking

---

## 🧠 Key Engineering Concepts Demonstrated

- Retrieval-Augmented Generation (RAG)
- Semantic search
- Vector databases
- LLM integration
- Prompt grounding
- Source attribution
- Enterprise knowledge retrieval
- Document processing
- Business workflow automation
- State-based request processing
- Streamlit application development
- API integration
- Environment/secrets management

---

## 🔮 Future Improvements

Potential production extensions include:

- Authentication and role-based access control
- PostgreSQL or another production database
- Email/Slack approval notifications
- Integration with enterprise ticketing systems
- Audit logs
- Multiple enterprise departments and workflows
- Advanced document chunking
- Hybrid keyword + semantic search
- Evaluation datasets for RAG accuracy
- Deployment using Docker and cloud infrastructure
- Observability and monitoring

---

## 📌 Project Status

**Core implementation complete.**

The current version demonstrates:

- Enterprise document-based question answering
- RAG-based retrieval
- LLM response generation
- Source attribution
- IT request creation
- Manager approval
- IT processing
- Request completion tracking

---

## 👨‍💻 Author

**Siva Charan**

Computer Science Engineering Student

GitHub: `sivacharan1366`