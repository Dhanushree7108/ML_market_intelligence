# ML Market Intelligence Project — Integrated Milestone 1 + Milestone 2

This personal project keeps **PostgreSQL** as the database and integrates Milestone 1 and Milestone 2 into one Streamlit dashboard.

## What is integrated

### Milestone 1 — Project & Market Intelligence
- Project input
- PostgreSQL project storage
- Existing project selection
- Market analysis
- TAM / SAM / SOM
- Market trends
- Competitor landscape

### Milestone 2 — Risk & Strategic Analysis
- Risk scoring engine
- Risk status
- Success probability
- Automatic SWOT analysis
- Project feasibility
- Groq AI recommendations
- Final integrated dashboard

The Milestone 1 Flask application is still preserved and can be run separately.

## Run the complete integrated application

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Open the Streamlit URL shown in the terminal, normally `http://localhost:8501`.

## Run Milestone 1 separately

```powershell
cd milestone1
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Run Milestone 2 separately

```powershell
cd milestone2
python -m streamlit run streamlit_app.py
```

## PostgreSQL

Both milestones use the same PostgreSQL `projects` table. No Supabase is used.

Create `.env` in the project root from `.env.example` and set your PostgreSQL password. Keep `.env` out of GitHub.

## Groq

Set `GROQ_API_KEY` in `.env` for local use. For Streamlit Cloud, put the key in Streamlit Secrets instead of committing it to GitHub.

## Important structure

```text
ML_market_intelligence_project/
├── streamlit_app.py             # ONE integrated M1 + M2 dashboard
├── requirements.txt
├── .env.example
├── milestone1/                   # Existing Flask + PostgreSQL milestone
│   ├── app.py
│   ├── database.py
│   ├── database.sql
│   └── ...
└── milestone2/                   # Risk/SWOT/Feasibility modules
    ├── streamlit_app.py          # M2-only runner
    ├── database.py               # PostgreSQL
    ├── risk_engine.py
    ├── swot_analysis.py
    ├── feasibility.py
    └── ...
```

**Main entry point for the combined project:** `streamlit_app.py`
