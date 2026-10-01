"""
ML_Market_Intelligence_Project - Milestone 1
Project Submission -> Flask -> PostgreSQL

Milestone 1 scope only:
  - Serve the project submission form
  - Validate + save the submitted project to PostgreSQL
  - Show a confirmation screen

Risk scoring / SWOT (Milestone 2), AI recommendations / LangGraph (Milestone 3),
and the full analytics dashboard (Milestone 4) are intentionally NOT part of
this file yet. The templates already carry the product's visual identity so
later milestones can slot straight in.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_connection
from market_analysis import get_dashboard_data

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"  # only used for flash messages in dev

# Fields collected in Milestone 1 (matches database.sql)
REQUIRED_FIELDS = [
    "project_name",
    "project_description",
    "target_market",
    "budget",
]
OPTIONAL_FIELDS = [
    "competition",
    "resources",
    "objectives",
]


@app.route("/")
def home():
    """Render the project submission form."""
    return render_template("project.html", active_stage="intake")


@app.route("/submit", methods=["POST"])
def submit_project():
    """Validate the submitted form and store it in PostgreSQL."""

    data = {field: request.form.get(field, "").strip() for field in REQUIRED_FIELDS + OPTIONAL_FIELDS}

    # --- basic server-side validation -------------------------------------
    missing = [f for f in REQUIRED_FIELDS if not data[f]]
    if missing:
        flash(f"Please fill in the required field(s): {', '.join(missing)}")
        return redirect(url_for("home"))

    try:
        budget_value = float(data["budget"])
        if budget_value < 0:
            raise ValueError
    except ValueError:
        flash("Budget must be a positive number.")
        return redirect(url_for("home"))

    # --- persist to PostgreSQL ----------------------------------------------
    connection = get_connection()
    cursor = connection.cursor()
    try:
        query = """
            INSERT INTO projects (
                project_name,
                project_description,
                target_market,
                budget,
                competition,
                resources,
                objectives
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(
            query,
            (
                data["project_name"],
                data["project_description"],
                data["target_market"],
                budget_value,
                data["competition"],
                data["resources"],
                data["objectives"],
            ),
        )
        new_id = cursor.fetchone()[0]
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return render_template(
        "success.html", project=data, budget=budget_value, project_id=new_id, active_stage="intake"
    )


@app.route("/dashboard")
def dashboard():
    """Market Analysis dashboard: latest submitted project + market data."""
    data = get_dashboard_data()

    latest_project = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT project_name, project_description, target_market, budget,
                   competition, resources, objectives
            FROM projects
            ORDER BY id DESC
            LIMIT 1
            """
        )
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        if row:
            latest_project = {
                "project_name": row[0],
                "project_description": row[1],
                "target_market": row[2],
                "budget": row[3],
                "competition": row[4],
                "resources": row[5],
                "objectives": row[6],
            }
    except Exception:
        latest_project = None

    return render_template(
        "dashboard.html",
        project=latest_project,
        market_size=data["market_size"],
        market_trends=data["market_trends"],
        competitors=data["competitors"],
        market_funnel=data["market_funnel"],
        active_stage="dashboard",
    )


@app.route("/risk-assessment")
def risk_assessment():
    return render_template(
        "placeholder.html",
        active_stage="risk",
        stage_index="02",
        title="Risk & SWOT",
        note="Risk scoring and the SWOT breakdown are built in Milestone 2. "
             "They'll read from the same projects table this form already writes to.",
    )


@app.route("/recommendations")
def recommendations():
    return render_template(
        "placeholder.html",
        active_stage="recommendations",
        stage_index="03",
        title="AI Recommendations",
        note="AI-generated recommendations, powered by LangGraph, are built in Milestone 3.",
    )


if __name__ == "__main__":
    app.run(debug=True)
