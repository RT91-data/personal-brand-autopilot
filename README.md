# ✍️ Personal Brand Autopilot

An AI-powered LinkedIn content generator built for D365/ERP consultants transitioning into AI Engineering.

Turns learning notes into market-standard LinkedIn posts — automatically, in your voice.

---

## What it does

- Reads learning notebooks directly from your GitHub repository
- Runs multi-step LLM pipeline with an agentic research step and LLM-as-judge evaluation to generate LinkedIn posts
- Scores each post on hook strength, D365 specificity, uniqueness, and impression
- Accepts feedback and regenerates until the post meets your standard
- Saves approved posts to a Notion content calendar with scheduled dates

---

## How it works

**Step 1 — Topic Selection**
User picks a topic from GitHub learning notebooks. Each notebook contains concept notes, D365 analogies, and post ideas built during the learning journey.

**Step 2 — Agent 0: Trend Spotter** *(agentic — uses web search)*
Searches what D365/AI practitioners are discussing this week. Surfaces recent Microsoft announcements and current debates to make the post timely, not just educational.

**Step 3 — Agent 1: Drafter** *(LLM)*
Generates raw insights and D365 scenarios from scratch using trend context as briefing. Never copies notebook content — the notes are context, not script.

**Step 4 — Agent 2: LinkedIn Strategist** *(LLM)*
Restructures draft for maximum LinkedIn performance. Applies story-first hook formula, mobile-first formatting, 150-200 word target.

**Step 5 — Agent 3: Voice Guardian** *(LLM)*
Applies Rupam's voice — senior consultant, not student. Removes generic AI language, corporate buzzwords, and motivational content.

**Step 6 — Agent 4: Quality Scorer** *(LLM-as-judge)*
Scores post on 4 dimensions: hook strength, D365 specificity, uniqueness, impression. Auto-retries full pipeline if any score is below 7 — up to 3 attempts.

**Step 7 — Notion Content Calendar**
Approved post saved with scheduled date, image suggestion, and quality scores for tracking over time.

---

**Auto-retry:** If any quality score is below 7, the pipeline reruns automatically with the scorer's fix suggestion as feedback — up to 3 attempts.

**Observability:** Every pipeline run traced in Langfuse — per-agent latency, token usage, and quality scores.

---

## Tech stack

- **Python** — core language
- **Streamlit** — UI
- **Anthropic Claude API** — 3-agent pipeline
- **GitHub API** — reads learning notebooks
- **Notion API** — content calendar

---

## Setup

**1. Clone the repo**

    git clone https://github.com/RT91-data/personal-brand-autopilot.git
    cd personal-brand-autopilot

**2. Create virtual environment**

    python -m venv venv
    venv\Scripts\activate

**3. Install dependencies**

    pip install -r requirements.txt

**4. Create .env file**

    ANTHROPIC_API_KEY=your_anthropic_api_key
    GITHUB_USERNAME=your_github_username
    GITHUB_REPO=your_learning_notes_repo
    NOTION_API_KEY=your_notion_integration_token
    NOTION_DATABASE_ID=your_notion_database_id
    LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
    LANGFUSE_SECRET_KEY=your_langfuse_secret_key
    LANGFUSE_HOST=https://cloud.langfuse.com

**Where to get each key:**
- `ANTHROPIC_API_KEY` — console.anthropic.com → API Keys
- `GITHUB_USERNAME` — your GitHub username
- `GITHUB_REPO` — your learning notes repo name
- `NOTION_API_KEY` — notion.so/my-integrations → create integration → copy token
- `NOTION_DATABASE_ID` — from your Notion LinkedIn Content Calendar database URL
- `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` — cloud.langfuse.com → project settings → API Keys
- `LANGFUSE_HOST` — always `https://cloud.langfuse.com` unless self-hosting

**5. Run the app**

    streamlit run app.py

---

## Project structure

    personal-brand-autopilot/
    ├── app.py                 # Main Streamlit UI
    ├── post_generator.py      # 3-agent pipeline
    ├── github_reader.py       # GitHub API integration
    ├── notion_saver.py        # Notion API integration
    ├── requirements.txt
    ├── .gitignore
    └── README.md

---

## Posts generated so far

| Topic | Score | Status |
|-------|-------|--------|
| What is Machine Learning | 9/10 | Ready to post |
| Supervised vs Unsupervised | 8/10 | Ready to post |

---

## Built by

**Rupam Tripathi** — D365 FnO/AX Technical Consultant, 14 years enterprise ERP experience, transitioning into AI Engineering.

[GitHub](https://github.com/RT91-data)