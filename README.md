# 𓂀 NileOracle — Ask the Ancient World Anything

> An AI-powered RAG chatbot for exploring Ancient Egyptian history, built on Bunson's *Encyclopedia of Ancient Egypt*, Groq (Llama 3.3 70B), LangChain, ChromaDB, and Flask.

![NileOracle Welcome Screen](screenshots/Screenshot%20(1).png)

---

## ✨ What It Does

**NileOracle** lets you have a natural conversation with an ancient Egyptian history encyclopedia. Ask about pharaohs, gods, dynasties, mummification, architecture, daily life — and get grounded, sourced answers with page references from the book.

It uses **Retrieval-Augmented Generation (RAG)**: your question is matched against embedded chunks of the encyclopedia, the most relevant passages are retrieved, and Llama 3.3 70B (via Groq's free API) generates a rich, accurate answer — telling you exactly which pages it drew from.

---

## 📸 Screenshots

### Welcome Screen
![Welcome](screenshots/Screenshot%20(1).png)

### Answering a Complex Question
![Timeline Response](screenshots/Screenshot%20(2).png)

### Multi-turn Conversation
![Conversation](screenshots/Screenshot%20(3).png)

---

## 🏗️ Architecture

```
User Question
     │
     ▼
ChromaDB Vector Search  ←── Bunson's Encyclopedia (481 pages, embedded)
     │
     ▼
Top 4 Relevant Chunks
     │
     ▼
Groq API (Llama 3.3 70B)  ←── Custom Egypt-focused prompt
     │
     ▼
Answer + Page References
     │
     ▼
Flask API → HTML/CSS/JS Frontend
```

| Component | Technology |
|---|---|
| LLM | Llama 3.3 70B via Groq (free) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector Store | ChromaDB |
| RAG Framework | LangChain (LCEL) |
| Backend | Flask |
| Frontend | HTML + CSS + Vanilla JS |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A free [Groq API key](https://console.groq.com)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/nile-oracle.git
cd nile-oracle
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Add your encyclopedia PDF
Place your copy of Bunson's *Encyclopedia of Ancient Egypt* in the root directory and name it:
```
encyclopedia.pdf
```

> ⚠️ The PDF is not included in this repository due to copyright. You must supply your own copy.

### 6. Build the vector database (run once)
```bash
python create_db.py
```
This embeds all 481 pages into ChromaDB. Takes 3–8 minutes. Only needs to run once — results are saved to `./chroma_db/`.

### 7. Launch the app
```bash
python app.py
```
Open your browser at **`http://127.0.0.1:5000`**

---

## 📁 Project Structure

```
nile-oracle/
├── app.py               # Flask backend + API routes
├── create_db.py         # One-time PDF indexing script
├── qa_chain.py          # LangChain RAG chain setup
├── encyclopedia.pdf     # Source material (not in repo)
├── requirements.txt
├── .env                 # API key — never committed
├── .gitignore
├── screenshots/         # UI screenshots for README
│   ├── Screenshot__1_.png
│   ├── Screenshot__2_.png
│   └── Screenshot__3_.png
└── static/
    └── index.html       # Full frontend (HTML + CSS + JS)
```

---

## 🔑 Getting a Free Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up with Google or email — no credit card required
3. Go to **API Keys** → **Create API Key**
4. Copy it into your `.env` file

**Free tier limits (as of 2026):**
- `llama-3.3-70b-versatile`: 1,000 requests/day, 12,000 tokens/minute
- More than enough for personal use and testing

---

## 🛠️ How RAG Works in NileOracle

1. **Indexing** (`create_db.py`): The encyclopedia PDF is split into 500-token chunks with 50-token overlaps. Each chunk is embedded using `all-MiniLM-L6-v2` and stored in ChromaDB.

2. **Retrieval** (`qa_chain.py`): When you ask a question, it's embedded using the same model. ChromaDB finds the 4 most semantically similar chunks.

3. **Generation**: The chunks are injected into a custom prompt and sent to Llama 3.3 70B on Groq. The model answers based on the encyclopedia first, falling back to general knowledge when needed.

4. **Attribution**: The page numbers of the retrieved chunks are returned alongside the answer.

---

## 🌐 Deployment

### Hugging Face Spaces
> Coming soon — deployment guide will be added in a future update.

---

## 🙏 Credits

- **Encyclopedia:** Bunson, Margaret R. *Encyclopedia of Ancient Egypt*. Facts on File, 2002.
- **LLM Inference:** [Groq](https://groq.com) — free, blazing-fast Llama 3.3 70B
- **RAG Framework:** [LangChain](https://langchain.com)
- **Vector Store:** [ChromaDB](https://trychroma.com)
- **Inspired by:** [MedBuddy](https://github.com/tararauzumaki/medbuddy)

---

## 📄 License

MIT License — feel free to fork, adapt, and build your own oracle.
