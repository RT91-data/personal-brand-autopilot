✍️ Personal Brand Autopilot

An AI-powered LinkedIn content generator built for D365/ERP consultants transitioning into AI Engineering.

Turns learning notes into market-standard LinkedIn posts — automatically, in your voice.

---

## What it does

- Reads learning notebooks directly from your GitHub repository
- Runs a 3-agent AI pipeline to generate LinkedIn posts
- Scores each post on hook strength, D365 specificity, uniqueness, and impression
- Accepts feedback and regenerates until the post meets your standard
- Saves approved posts to a Notion content calendar with scheduled dates

---

## How it works
GitHub Notebooks
↓
Agent 1: Drafter — extracts best angle, generates own examples
↓
Agent 2: LinkedIn Strategist — structures for maximum performance
↓
Agent 3: Voice Guardian — applies your voice, removes generic AI language
↓
Quality Scorer — scores 4 dimensions, flags weak posts
↓
Notion Content Calendar — saved with topic, date, image suggestion
---

## Tech stack

- Python
- Streamlit — UI
- Anthropic Claude API — 3-agent pipeline
- GitHub API — reads learning notebooks
- Notion API — content calendar

---

## Setup

**1. Clone the repo:**
```bash
git clone https://github.com/RT91-data/personal-brand-autopilot.git
cd personal-brand-autopilot
```

**2. Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file:**
ANTHROPIC_API_KEY=your_anthropic_api_key
GITHUB_USERNAME=your_github_username
GITHUB_REPO=your_learning_notes_repo
NOTION_API_KEY=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id

**5. Run the app:**
```bash
streamlit run app.py
```

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
| What is Machine Learning | 9.5/10 | Ready to post |
| Supervised vs Unsupervised | 10/10 | Ready to post |

---

## Built by

**Rupam Tripathi** — D365 FnO/AX Technical Consultant, 14 years enterprise ERP experience, transitioning into AI Engineering.

[GitHub](https://github.com/RT91-data)
