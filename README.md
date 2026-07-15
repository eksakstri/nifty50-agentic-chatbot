# 📈 Nifty50 Agentic Chatbot

An **Agentic Retrieval-Augmented Generation (RAG)** chatbot for the Indian stock market that answers questions about **NIFTY 50 companies**, **live market performance**, **option chain data**, and **corporate announcements** using **LangGraph**, **FAISS**, and **Groq LLMs**.

Unlike traditional RAG systems that search a single knowledge base, this chatbot intelligently routes user queries to the most appropriate information source before generating an answer.

---

## ✨ Features

* 📊 Live NIFTY 50 market snapshot analysis
* 📈 Option Chain analysis
* 📄 Corporate announcement understanding using semantic search
* 🤖 Agentic routing using LangGraph
* 🔍 FAISS-powered document retrieval
* ⚡ Groq LLM for fast inference
* 🧠 Multi-tool decision making
* 📚 Source-aware responses with confidence gating
* ☁️ Automatically downloads the latest retrieval assets from Hugging Face

---

## 🏗 Architecture

```text
                          User Query
                               │
                               ▼
                       LangGraph Router
                               │
      ┌───────────────┬───────────────┬───────────────┐
      │               │               │               │
      ▼               ▼               ▼               ▼
 Market Data     Option Chain      PDF Search     General LLM
 Retriever        Retriever       (FAISS RAG)      Response
      │               │               │
      └───────────────┴───────────────┘
                      │
                      ▼
              Answer Generator (Groq)
                      │
                      ▼
                Final User Response
```

---

## 📂 Project Structure

```text
nifty50-agentic-chatbot/

│
├── app.py
├── main.py
├── graph.py
├── state.py
├── config.py
├── download_assets.py
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

## 🧠 How It Works

The chatbot first classifies every user query into one of four categories:

### 1. Market Data

Uses the latest NIFTY 50 market snapshot to answer questions such as:

* Top gainers today
* Biggest losers
* Company performance
* Price movement
* Trading volume
* Daily market summary

---

### 2. Option Chain

Uses the latest Option Chain CSV to answer questions about:

* Open Interest
* Change in OI
* Max Pain
* PCR
* ITM/OTM contracts
* Strike analysis
* Support and resistance

---

### 3. Corporate Announcements

Uses Retrieval-Augmented Generation over downloaded company announcements.

Pipeline:

```text
Query
    ↓
FAISS Similarity Search
    ↓
Top Relevant Chunks
    ↓
Groq LLM
    ↓
Grounded Response
```

---

### 4. General Queries

Questions outside the supported financial domain are answered directly by the LLM.

The chatbot clearly indicates when a response is based on general knowledge rather than retrieved company data.

---

## 📦 Data Source

This project does **not** store embeddings or market files inside the repository.

At startup it downloads the latest retrieval assets from the companion Hugging Face Dataset.

Dataset:

`eksakstri/nifty50-rag-data`

The dataset contains:

* `corpus.faiss`
* `chunk_metadata.json`
* `company_summaries.md`
* `nifty50_snapshot.json`
* `option_chain.csv`

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/<username>/nifty50-agentic-chatbot.git

cd nifty50-agentic-chatbot
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
GROQ_API_KEY=your_api_key
HF_DATASET=eksakstri/nifty50-rag-data
```

Run the chatbot

```bash
streamlit run app.py
```

The required retrieval assets are downloaded automatically on first launch.

---

## 💬 Example Questions

### Market

* Which stock gained the most today?
* Show today's top losers.
* How did HDFC Bank perform today?
* Which stock traded the highest volume?

### Option Chain

* Where is the maximum Call Open Interest?
* What is the current market sentiment?
* Which strike has the highest Put OI?
* Explain today's option chain.

### Corporate Announcements

* Summarize Reliance's latest announcement.
* What has Infosys recently announced?
* Has TCS released any new corporate filings?
* Explain HDFC Bank's recent disclosure.

---

## 🛠 Tech Stack

* Python
* LangGraph
* FAISS
* Sentence Transformers
* Groq API
* Streamlit
* Hugging Face Hub
* Pandas
* NumPy

---

## 🔄 Related Projects

### 📊 Nifty50 Data Pipeline

A separate data engineering pipeline responsible for:

* Collecting live NSE market data
* Downloading corporate announcement PDFs
* Generating semantic embeddings
* Building FAISS indices
* Publishing retrieval assets to Hugging Face

Repository:

`nifty50-data-pipeline`

---

## 🚧 Future Improvements

* Conversation memory
* Citation highlighting
* Streaming responses
* Hybrid keyword + vector retrieval
* Query rewriting
* Incremental FAISS updates
* Multi-agent financial analysis

---

## 📜 License

MIT License
