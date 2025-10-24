# 🧠 TakeForge — Opinion Intelligence Agent

**TakeForge** turns sports articles into structured **takes** (headline + explanation), enriches them with **metadata**, stores them in a vector DB, and exposes a unified **/ask** endpoint that can either **answer** a focused question or **summarize** themes across takes.

- 🔎 Extraction & metadata (LLM)
- 🔁 Background worker that processes articles on app startup
- 🔍 Vector retrieval + metadata re-ranking (hybrid)
- 🤖 Mode-aware AskAgent (query vs summary)
- 🧰 Clean Python modules; FastAPI service

---

## 📁 Project Structure (actual)

```
take_forge/
├── api/
│   ├── deps.py                 # Startup hooks: launches background take-extraction thread
│   └── v1.py                   # FastAPI routes (/api/v1/ask)
│
├── ask_agent/
│   ├── ask_agent.py            # Unified entrypoint: analyze → retrieve → prompt LLM
│   ├── query_analyzer.py       # Detects mode (query|summary) + builds soft filters
│   └── tools/
│       ├── query_pipeline.py   # Vector search (top-N) + metadata re-rank (precision)
│       ├── summary_pipeline.py # Vector search (broad) + metadata re-rank (recall)
│       └── re_ranker.py        # Shared scoring utility (tags/entities/tone/stance)
│
├── core/
│   └── openai_client.py        # Centralized OpenAI client (reads OPENAI_API_KEY)
│
├── opinion_agent/
│   ├── metadata_utils.py       # normalize_metadata() + flatten for Chroma
│   ├── opinion_agent.py        # Extracts takes + per-take metadata
│   └── prompt_utils.py         # Prompt builders for take + metadata generation
│
├── scraper_service/
│   └── scraper.py              # Iterates demo articles (next_article())
│
├── vector_store/
│   └── chroma_store.py         # Chroma wrapper (add_take, query, de-dup keys)
│
├── data/                       # mock articles live here (for demo)
├── models.py                   # Pydantic/shared models
├── main.py                     # FastAPI app factory / include_router
├── .env                        # OPENAI_API_KEY=...
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
# 1) Create venv
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows PowerShell
# .\venv\Scripts\Activate.ps1

# 2) Install deps
pip install -r requirements.txt

# 3) Configure environment
# Put your key in .env (same directory as main.py)
# OPENAI_API_KEY=sk-...

# 4) Run the API (dev)
python main.py
```

> The app reads **.env** automatically (via your code). Make sure `OPENAI_API_KEY` is present.

---

## 🚀 How it Works at Runtime

### 1) Background worker (auto-start)

- **`api/deps.py`** registers a startup hook (FastAPI lifespan/on_startup) that spawns a **background thread**.
- That thread loops over `scraper_service.scraper.next_article()` → calls `opinion_agent.opinion_agent.extract_takes()` → **generates takes + metadata** → stores via `vector_store.chroma_store.add_take()`.
- You’ll see console logs like:

  - `[TakeForge] art001: 3 takes`
  - `metadata: {...}`
  - `[TakeForge] Stored 3 takes for art001`

> You **do not** run a separate script. The worker runs automatically whenever the API boots.

### 2) Ask endpoint

- **Route:** `GET /api/v1/ask?q=...`

- **Flow:** `ask_agent.ask_agent.AskAgent.ask(query)`

  1. `query_analyzer.analyze_query()` → decides **mode** (`query` or `summary`) + soft filters
  2. Runs **query_pipeline** (precision) or **summary_pipeline** (recall)
  3. Vector results are **re-ranked** with `re_ranker.score_metadata()` using tags/entities/tone/stance
  4. Builds a **structured context**:
     `[relevance_score=0.92] [tags=...] [published_at=YYYY-MM-DD] <take>`
  5. Mode-specific prompt → **LLM answer**

- **Example:**

  ```bash
  curl "http://localhost:8080/api/v1/ask?q=What%20do%20analysts%20say%20about%20Kyrie%20Irving%E2%80%99s%20impact%20on%20the%20Mavericks%20offense?"
  ```

---

## 🧪 Quick Test Queries

- **Query:**
  `What do analysts say about Kyrie Irving’s impact on the Mavericks offense?`
- **Query:**
  `How is Luka Doncic affected by Kyrie Irving’s return?`
- **Summary:**
  `Summarize recent opinions about Zion Williamson’s durability and health management.`
- **Summary:**
  `Summarize analyst views on Celtics chemistry and playoff readiness.`
- **Query (alias normalization):**
  `What do people think about Joe Mazzulla’s coaching strategy this season?`
- **Query (implicit entity):**
  `How is Wemby’s second NBA season being described by analysts?`

---

## 🧠 Key Design Choices

- **Re-ranking over strict metadata filters (Chroma):**
  Chroma’s metadata filtering doesn’t support list/substring operators for `tags/entities`.
  We do **vector-first retrieval** and **Python re-ranking** by overlap with `tags/entities` (+ tone/stance).
  This keeps results tight while staying Chroma-compatible.

- **Mode-aware prompting:**

  - **Query:** short, evidence-based answer (2–5 sentences)
  - **Summary:** neutral synthesis (3–6 sentences), **uses `published_at`** to reflect recency/trends

- **De-dup & IDs:**
  Each take uses a deterministic ID (e.g., `f"{article_id}:{take_idx}"`) to avoid duplication across runs.

- **Agent split:**
  `OpinionAgent` (extraction pipeline) and `AskAgent` (retrieval + LLM) are **separate** for clarity and testing.

---

## 🗺️ Roadmap

- ✅ MVP: Chroma + re-ranker (done)
- 🔁 Switch to **Qdrant** or **Pincone** for native `match.any` over `tags/entities`
- 🧭 Add `/search` endpoint with filter controls (tone, stance, entity)
- 🖥️ Simple UI (React) to browse takes and ask questions
- 🧪 Eval harness (gold Q/A pairs vs. model outputs)

---

## 🛡️ Notes & Limits

- This is a demo; article sources are mock data. Swap in your real scraper.
- Chroma is used with a re-ranker due to metadata filter limitations.
- Make sure you comply with API key handling and logging hygiene.

---
