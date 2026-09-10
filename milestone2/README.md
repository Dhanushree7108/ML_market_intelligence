# Milestone 2 — Risk Assessment & SWOT (Streamlit)

This folder contains **only the Milestone 2 implementation**. It does not
modify Milestone 1 Flask files.

Run from this folder:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app reads the existing Milestone 1 PostgreSQL `projects` table and provides
Project Input, Risk Assessment, SWOT, Feasibility, Recommendations and a
dashboard-style view.

Create `.env` at the project root (one level above `milestone2`) using the
same database settings as Milestone 1. Never commit `.env`.
