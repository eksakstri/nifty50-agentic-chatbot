---
title: NIFTY50 Agentic Chatbot
emoji: 📈
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.38.0
app_file: app.py
pinned: false
license: mit
---
# 📈 NIFTY50 Agentic Chatbot

An **Agentic Retrieval-Augmented Generation (RAG)** chatbot for the Indian stock market that intelligently answers questions about **NIFTY 50 companies**, **market performance**, **option chain data**, and **corporate announcements**.

Unlike a traditional RAG chatbot, this project uses **LangGraph** to dynamically route each query to the appropriate data source before generating a grounded response.

---

## ✨ Features

* 🤖 Agentic routing using LangGraph
* 📊 Live NIFTY 50 market analysis
* 📈 Option Chain interpretation
* 📄 Corporate announcement retrieval using FAISS
* 🔍 Semantic search over company filings
* ⚡ Groq LLM powered response generation
* 🧠 Multi-tool decision making
* 📚 Confidence-gated grounded answers
* ☁️ Automatic retrieval asset download from Hugging Face Dataset
* 🌐 Interactive Gradio web interface

---

# 🏗 System Architecture

```text
                              User Query
                                   │
                                   ▼
                           Gradio Interface
                                   │
                                   ▼
                           LangGraph Router
                                   │
      ┌───────────────────┬───────────────┬───────────────────┐
      │                   │               │                   │
      ▼                   ▼               ▼                   ▼
 Market Retriever   Option Chain     PDF Retriever      General LLM
                    Retriever        (FAISS Search)
      │                   │               │
      └───────────────────┴───────────────┘
                      Retrieved Context
                              │
                              ▼
                     Answer Generator (Groq)
                              │
                              ▼
                       Final User Response
```

---

# 🗂 Project Structure

```text
nifty50-agentic-chatbot/

│
├── app.py                     # Gradio interface
├── main.py                    # Chatbot initialization
├── graph.py                   # LangGraph workflow
├── state.py                   # Shared graph state
├── config.py                  # Configuration & environment variables
├── download_assets.py         # Downloads retrieval assets
│
├── agent/
│   ├── router.py
│   ├── router_node.py
│   ├── answer_generator.py
│   └── nodes/
│
├── retrievers/
│   ├── market_retriever.py
│   ├── option_chain_retriever.py
│   └── pdf_retriever.py
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# 🧠 Workflow

Every user question first passes through a routing agent.

The router classifies the query into one of four categories.

## 📊 Market Data

Uses the latest NIFTY50 market snapshot.

Typical questions:

* Top gainers today
* Biggest losers today
* How did HDFC Bank perform today?
* Highest traded volume
* Daily market performance
* Company price movement

---

## 📈 Option Chain

Uses the latest downloaded Option Chain CSV.

Typical questions:

* Maximum Call Open Interest
* Maximum Put Open Interest
* PCR
* Support & Resistance
* Strike analysis
* Option chain sentiment

---

## 📄 Corporate Announcements

Uses semantic search over downloaded corporate announcement PDFs.

Pipeline

```text
User Query
      │
      ▼
FAISS Similarity Search
      │
      ▼
Relevant Chunks
      │
      ▼
Groq LLM
      │
      ▼
Grounded Response
```

Typical questions:

* Summarize Reliance's latest announcement.
* Has Infosys released any filings recently?
* Explain today's HDFC Bank announcement.

---

## 💬 General Finance

If the question is outside the supported retrieval sources, the chatbot responds using the LLM's general knowledge while clearly indicating that the answer is not based on retrieved company data.

---

# 📦 Data Source

This repository intentionally **does not contain**:

* PDF documents
* FAISS index
* Embeddings
* Metadata
* Market snapshot
* Option chain CSV

Instead, the application automatically downloads the latest retrieval assets from the companion Hugging Face Dataset during startup.

Dataset:

**eksakstri/nifty50-rag-data**

Downloaded assets include:

* corpus.faiss
* chunk_metadata.json
* company_summaries.md
* nifty50_snapshot.json
* option_chain.csv

This keeps the repository lightweight while ensuring the chatbot always uses the latest generated data.

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/<your_username>/nifty50-agentic-chatbot.git

cd nifty50-agentic-chatbot
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key

HF_DATASET=eksakstri/nifty50-rag-data
```

Run the application

```bash
python app.py
```

The retrieval assets will automatically be downloaded during the first startup.

---

# 💬 Example Questions

## Market

* Which stock gained the most today?
* Show today's top losers.
* Which company had the highest trading volume?
* How did Reliance perform today?

---

## Option Chain

* Where is the maximum Call Open Interest?
* What is the market sentiment today?
* Which strike has the highest Put OI?
* Explain today's option chain.

---

## Corporate Announcements

* Summarize Reliance's latest announcement.
* Explain Infosys' recent filing.
* What has TCS announced recently?
* Has HDFC Bank released any disclosures today?

---

# 🛠 Technology Stack

* Python
* LangGraph
* Gradio
* FAISS
* Sentence Transformers
* Groq API
* Hugging Face Hub
* NumPy
* Pandas

---

# 🌐 Deployment

The application is designed to be deployed on **Hugging Face Spaces**.

Startup sequence:

```text
Launch Application
        │
        ▼
Download Retrieval Assets
        │
        ▼
Load FAISS Index
        │
        ▼
Load Metadata
        │
        ▼
Initialize LangGraph
        │
        ▼
Launch Gradio Interface
```

---

# 🔄 Project Ecosystem

```text
                    ┌──────────────────────────────┐
                    │ Nifty50 Data Pipeline        │
                    │ (GitHub Repository)          │
                    └──────────────┬───────────────┘
                                   │
                      Generates embeddings & market data
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ Hugging Face Dataset         │
                    │ nifty50-rag-data            │
                    └──────────────┬───────────────┘
                                   │
                          download_assets.py
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ Nifty50 Agentic Chatbot      │
                    │ (GitHub + HF Spaces)         │
                    └──────────────────────────────┘
```

---

# 🚧 Future Improvements

* Multi-turn conversation memory
* Streaming responses
* Source citations
* Interactive stock charts
* Hybrid keyword + vector retrieval
* Query rewriting
* Incremental FAISS updates
* Portfolio analysis
* Multi-agent financial reasoning

---

# 📸 Demo

A live demo will be available through Hugging Face Spaces.

---

# 🔗 Related Projects

### Nifty50 Data Pipeline

Responsible for:

* Downloading NSE market data
* Downloading corporate announcement PDFs
* Building semantic embeddings
* Creating the FAISS index
* Publishing retrieval assets to Hugging Face

Repository:

`nifty50-data-pipeline`

---

# 📄 License

This project is licensed under the MIT License.
