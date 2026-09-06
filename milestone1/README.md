# ML_Market_Intelligence_Project — Milestone 1 + Dashboard

**Core scope:** Project Submission Form → Flask → PostgreSQL → data stored.
**Plus:** a Dashboard page (Market Analysis + Competitor Landscape) that reads the most
recently submitted project and shows it alongside market data. Risk scoring & SWOT are
still Milestone 2, and AI recommendations / LangGraph are still Milestone 3 — the
Dashboard here is the Market Analysis piece, using fixed demo figures until a later
milestone computes them for real.

```
ML_Market_Intelligence_Project/
│
├── app.py                 # Flask routes: "/" (form), "/submit" (save), "/dashboard",
│                           #   "/risk-assessment", "/recommendations"
├── database.py             # PostgreSQL connection helper (reads .env)
├── database.sql            # CREATE TABLE for Milestone 1
├── market_analysis.py      # TAM/SAM/SOM, funnel, trend series, competitor data
├── requirements.txt
├── .env.example             # copy to .env and fill in your Postgres password
├── README.md
│
├── templates/
│   ├── base.html           # shared layout + milestone roadmap rail
│   ├── project.html        # the submission form (Stage 01 · Project Intake)
│   ├── success.html        # confirmation screen after saving
│   ├── dashboard.html      # Market Analysis dashboard (Stage 04)
│   └── placeholder.html    # "coming up next" screen for Stages 02 & 03
│
└── static/
    ├── css/style.css        # visual identity for the whole platform
    └── js/
        ├── main.js          # client-side field validation polish
        └── dashboard.js     # renders all 3 dashboard charts (Chart.js via CDN)
```

Every stage in the sidebar is now a real, clickable route — Stages 02 (Risk & SWOT) and
03 (AI Recommendations) go to a "coming up next" placeholder page instead of being
dead/locked links, so the navigation is fully wired even before those milestones ship.

## Dashboard

Visit `http://127.0.0.1:5000/dashboard` (or click **View market dashboard** after
submitting a project, or **04 · Dashboard** in the sidebar). Each section has its own
accent color — teal for your submission, violet for market sizing, coral for
competitors — so the three panels read as distinct at a glance:

- **Project Submission** (teal) — the most recently submitted project's name, target market, budget, and description.
- **Market Analysis** (violet) — TAM / SAM / SOM stat cards, a TAM→SAM→SOM funnel visual, and a 2020–2026 market trends line chart.
- **Competitor Landscape** (coral) — a market-share doughnut chart, a revenue bar chart, and per-competitor cards with share/revenue/growth.

The market figures come from `market_analysis.py` as static demo values for now. When a
real market-sizing calculation exists, only that file needs to change — the route and
template already expect the same shape of data.

---

## Run it in VS Code, step by step

### 1. Install prerequisites (once per machine)
- **Python 3.x** — [python.org/downloads](https://www.python.org/downloads/). On the
  Windows installer, tick **Add Python to PATH** before clicking Install.
- **VS Code** — [code.visualstudio.com](https://code.visualstudio.com/). Once open,
  go to the Extensions panel and install the **Python** extension (by Microsoft).
- **PostgreSQL** — [postgresql.org/download](https://www.postgresql.org/download/).
  During install you'll set a password for the `postgres` user — remember it, you'll
  need it in step 5.

Check Python installed correctly:
```bash
python --version
```

### 2. Open the project folder
In VS Code: **File → Open Folder…** → select `ML_Market_Intelligence_Project`.
Then open a terminal: **Terminal → New Terminal**.

### 3. Create and activate a virtual environment
```bash
python -m venv venv
```
Activate it:
- **Windows:** `venv\Scripts\activate`
- **macOS/Linux:** `source venv/bin/activate`

You should see `(venv)` at the start of your terminal prompt. VS Code may also prompt
"Select environment for this workspace" in the bottom right — pick the `venv` one.

### 4. Install the Python packages
```bash
pip install -r requirements.txt
```
This installs Flask, psycopg (PostgreSQL driver), and python-dotenv.

### 5. Create the PostgreSQL database and table
Open **pgAdmin 4** (installed alongside PostgreSQL).
1. Right-click **Databases → Create → Database…**, name it `ml_project`.
2. Select `ml_project` → **Query Tool**.
3. Open `database.sql` from this project (or paste its contents) and click **Execute (▶)**.

You should now have a `projects` table with these columns: `id`, `project_name`,
`project_description`, `target_market`, `budget`, `competition`, `resources`,
`objectives`, `created_at`.

### 6. Configure your database password
Copy `.env.example` to a new file named `.env` in the same folder, then edit it:
```
DB_HOST=localhost
DB_NAME=ml_project
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
DB_PORT=5432
```
Replace `YOUR_POSTGRES_PASSWORD` with the password you set during PostgreSQL install.
`.env` keeps the password out of the source code — don't commit it.

### 7. Run the app
```bash
python app.py
```
You should see:
```
Running on http://127.0.0.1:5000
```
Open that address in your browser.

### 8. Test it with sample data
| Field | Sample value |
|---|---|
| Project name | Online College Food Delivery |
| Project description | A platform for students to order food from nearby food providers. |
| Target market | College students |
| Budget | 50000 |
| Competition | Existing food delivery platforms |
| Resources | Student development team |
| Objectives | Provide convenient food ordering for students |

Click **Submit project** — you should land on a confirmation screen showing the record
that was saved, with its new database `id`.

### 9. View the Dashboard
From the confirmation screen, click **View market dashboard** (or go to
`http://127.0.0.1:5000/dashboard`, or click **04 · Dashboard** in the sidebar). You
should see your submitted project summarised next to the Market Analysis stat cards,
the trends chart, and the Competitor Landscape.

### 10. Verify the row landed in PostgreSQL
Back in pgAdmin, Query Tool on `ml_project`:
```sql
SELECT * FROM projects ORDER BY id DESC;
```
Your submitted project should be the top row.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `ModuleNotFoundError: flask` | Virtual environment isn't activated, or step 4 wasn't run in it. |
| `psycopg.OperationalError: password authentication failed` | Wrong password in `.env`. |
| `psycopg.OperationalError: database "ml_project" does not exist` | Step 5 wasn't completed, or the database name doesn't match `.env`. |
| Form submits but page shows a Flask traceback about a missing column | `database.sql` wasn't run, or was run against the wrong database. |
| Port 5000 already in use | Stop whatever else is using it, or run `app.run(debug=True, port=5001)` and browse to `:5001`. |

## What's next
Milestone 2 will read from this same `projects` table to compute a risk score and a
SWOT breakdown — no changes to this milestone's schema should be needed, only additive
tables/columns.
