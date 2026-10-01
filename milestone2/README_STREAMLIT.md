# ML Market Intelligence Project — Milestone 2 (Streamlit)

This version adds the **Milestone 2 Risk Assessment & SWOT Analysis UI in Streamlit**, while keeping the existing Milestone 1 PostgreSQL project and Flask files.

## Milestone 2 included

- Market Competition
- Team Expertise
- Resource Availability
- Innovation Level
- Market Research
- Risk Score
- Risk Status
- Success Probability
- SWOT Analysis
- Project Feasibility using four 0–100 sliders

The scoring rules are implemented in `risk_engine.py`, `swot_analysis.py`, and `feasibility.py` according to the Milestone 2 plan.

## Run Streamlit

Open PowerShell in this folder and activate the virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If your Python installation says that pip is missing:

```powershell
python -m ensurepip --upgrade
python -m pip install -r requirements.txt
```

Create `.env` from `.env.example` and enter your PostgreSQL password.

Make sure the `ml_project` database and `projects` table from `database.sql` exist.

Run Milestone 2:

```powershell
streamlit run streamlit_app.py
```

The browser should open the Streamlit app automatically (normally on `http://localhost:8501`).

## Important

Milestone 2 feasibility is **input-based/manual**, as specified in the plan: the user adjusts four sliders and the application calculates their average. It is not an AI prediction in this milestone.

Milestone 3 AI recommendations/LangGraph are intentionally not included.
