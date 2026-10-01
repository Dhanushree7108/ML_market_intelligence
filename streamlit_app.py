"""Integrated ML Market Intelligence application.

Milestone 1: project input + PostgreSQL storage + market intelligence.
Milestone 2: risk assessment + SWOT + feasibility + Groq recommendations.

The Flask Milestone 1 application remains available separately in milestone1/app.py.
This Streamlit application is the integrated dashboard using the same PostgreSQL
projects table.
"""

import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Reuse the existing Milestone 2 modules without changing Milestone 1.
M2_DIR = Path(__file__).resolve().parent / "milestone2"
if str(M2_DIR) not in sys.path:
    sys.path.insert(0, str(M2_DIR))

from database import fetch_projects, insert_project  # noqa: E402
from risk_engine import (  # noqa: E402
    calculate_risk,
    calculate_success_probability,
    get_risk_status,
    risk_breakdown,
)
from swot_analysis import generate_swot  # noqa: E402
from feasibility import calculate_feasibility, feasibility_label  # noqa: E402
from market_analysis import get_market_size, get_market_trends, get_competitors  # noqa: E402


st.set_page_config(
    page_title="ML Market Intelligence",
    page_icon="ðŸ“Š",
    layout="wide",
    initial_sidebar_state="expanded",
)


def setting(name, default=None):
    value = os.getenv(name)
    if value:
        return value
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return default


def load_projects():
    try:
        return fetch_projects(), None
    except Exception as exc:
        return [], str(exc)


def project_dict(row):
    return {
        "id": row[0],
        "project_name": row[1],
        "project_description": row[2],
        "target_market": row[3],
        "budget": row[4],
        "competition": row[5] or "",
        "resources": row[6] or "",
        "objectives": row[7] or "",
        "created_at": row[8],
    }


def project_competition_default(project):
    text = (project or {}).get("competition", "").strip().lower()
    if text in {"low", "medium", "high"}:
        return {"low": 0, "medium": 1, "high": 2}[text]
    return 1


def project_resource_default(project):
    text = (project or {}).get("resources", "").strip().lower()
    if text in {"limited", "moderate", "good"}:
        return {"limited": 0, "moderate": 1, "good": 2}[text]
    return 1


def run_assessment(inputs):
    risk_score = calculate_risk(**inputs["risk"])
    swot = generate_swot(
        inputs["risk"]["team_expertise"],
        inputs["risk"]["innovation_level"],
        inputs["risk"]["market_competition"],
        inputs["risk"]["resource_availability"],
        inputs["risk"]["market_research"],
    )
    feasibility = calculate_feasibility(**inputs["feasibility"])
    return {
        "risk_score": risk_score,
        "risk_status": get_risk_status(risk_score),
        "success_probability": calculate_success_probability(risk_score),
        "breakdown": risk_breakdown(**inputs["risk"]),
        "swot": swot,
        "feasibility_score": feasibility,
        "feasibility_label": feasibility_label(feasibility),
        "inputs": inputs,
    }


def groq_recommendation(project, result):
    key = setting("GROQ_API_KEY")
    if not key:
        return None, "GROQ_API_KEY is not configured. Add it to your local .env or Streamlit Secrets."

    try:
        from groq import Groq

        client = Groq(api_key=key)
        project = project or {}
        prompt = f"""
You are an AI business analyst for a student ML Market Intelligence project.
Use only the supplied project and assessment information. Do not invent market
facts, competitor data, financial statistics, or claims not present below.

Project: {project.get('project_name', 'Not provided')}
Target market: {project.get('target_market', 'Not provided')}
Description: {project.get('project_description', 'Not provided')}
Budget: {project.get('budget', 'Not provided')}

Risk score: {result['risk_score']}/100
Risk status: {result['risk_status']}
Success probability: {result['success_probability']}%
Feasibility: {result['feasibility_score']}% ({result['feasibility_label']})
SWOT: {result['swot']}

Return concise sections:
1. Executive assessment
2. Top 3 actions to reduce risk
3. How to strengthen feasibility
4. How to use strengths and opportunities
5. Key risks to monitor
"""
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a concise business analysis assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=700,
        )
        return response.choices[0].message.content, None
    except Exception as exc:
        return None, f"Groq request failed: {exc}"


def show_project_card(project):
    if not project:
        st.info("No project selected yet.")
        return
    c1, c2, c3 = st.columns(3)
    c1.metric("Project", project["project_name"])
    c2.metric("Target Market", project["target_market"])
    c3.metric("Budget", f"â‚¹{float(project['budget']):,.2f}")
    st.write(f"**Description:** {project['project_description']}")
    a, b, c = st.columns(3)
    a.write(f"**Competition:** {project['competition'] or 'Not provided'}")
    b.write(f"**Resources:** {project['resources'] or 'Not provided'}")
    c.write(f"**Objectives:** {project['objectives'] or 'Not provided'}")


def display_swot(swot):
    left, right = st.columns(2)
    with left:
        st.markdown("### ðŸ’ª Strengths")
        for item in swot["Strengths"]:
            st.success(f"â€¢ {item}")
        st.markdown("### ðŸš€ Opportunities")
        for item in swot["Opportunities"]:
            st.info(f"â€¢ {item}")
    with right:
        st.markdown("### âš ï¸ Weaknesses")
        for item in swot["Weaknesses"]:
            st.warning(f"â€¢ {item}")
        st.markdown("### ðŸ›¡ï¸ Threats")
        for item in swot["Threats"]:
            st.error(f"â€¢ {item}")


# ---------- Header ----------
st.title("ML Market Intelligence")
st.subheader("Project Data Collection â€¢ Market Intelligence â€¢ Risk Assessment â€¢ SWOT â€¢ Feasibility")
st.caption("Integrated Milestone 1 + Milestone 2 | PostgreSQL | Streamlit | Groq AI")
st.divider()

projects, db_error = load_projects()

with st.sidebar:
    st.header("Project Navigation")
    st.success("PostgreSQL backend") if not db_error else st.error("PostgreSQL connection failed")

    st.markdown("### 📋 Project Input")
    st.caption("Milestone 1")

    st.markdown("### 📊 Market Intelligence")
    st.caption("Milestone 1")

    st.markdown("### ⚠️ Risk & SWOT")
    st.caption("Milestone 2")

    st.markdown("### 🤖 AI Recommendations")
    st.caption("Milestone 2")

    st.markdown("### 📈 Final Dashboard")
    st.caption("Milestone 1 + Milestone 2")
tabs = st.tabs([
    "📋 Project Input",
    "📊 Market Intelligence",
    "⚠️ Risk & SWOT",
    "🤖 AI Recommendations",
    "📈 Final Dashboard",
])
# ---------- Milestone 1: Project Input ----------
with tabs[0]:
    st.header("Milestone 1 â€” Project Input")
    st.write("Enter and store project information in the existing PostgreSQL projects table.")

    selected = None
    if projects:
        labels = [f"{r[1]} â€” {r[3]} â€” â‚¹{float(r[4]):,.2f}" for r in projects]
        selected_index = st.selectbox(
            "Select an existing Milestone 1 project",
            range(len(labels)),
            format_func=lambda i: labels[i],
        )
        selected = project_dict(projects[selected_index])
        st.session_state["selected_project"] = selected
        st.markdown("### Selected Project")
        show_project_card(selected)
    else:
        st.info("No project found. Add your first project below.")

    with st.expander("âž• Add New Project to PostgreSQL", expanded=not bool(projects)):
        with st.form("integrated_project_form"):
            name = st.text_input("Startup / Project Name *")
            target_market = st.text_input("Target Market *")
            budget = st.number_input("Budget (â‚¹)", min_value=0.0, step=1000.0)
            description = st.text_area("Project Description *")
            competition = st.selectbox("Competition", ["Low", "Medium", "High"])
            resources = st.selectbox("Resources", ["Limited", "Moderate", "Good"])
            objectives = st.text_area("Objectives")
            save = st.form_submit_button("Save Project", type="primary", use_container_width=True)

            if save:
                if not name or not target_market or not description:
                    st.error("Please fill the required fields marked with *.")
                else:
                    try:
                        new_id = insert_project(
                            name,
                            description,
                            target_market,
                            budget,
                            competition,
                            resources,
                            objectives,
                        )
                        st.success(f"Project saved successfully in PostgreSQL. ID: {new_id}")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not save project: {exc}")

# ---------- Milestone 1: Market Intelligence ----------
with tabs[1]:
    st.header("Milestone 1 â€” Market Intelligence")
    project = st.session_state.get("selected_project")
    if project is None and projects:
        project = project_dict(projects[0])
        st.session_state["selected_project"] = project

    show_project_card(project)
    st.divider()

    market = get_market_size()
    a, b, c = st.columns(3)
    a.metric("TAM", market["tam"]["value"])
    b.metric("SAM", market["sam"]["value"])
    c.metric("SOM", market["som"]["value"])

    trend = get_market_trends()
    chart_df = pd.DataFrame({"Estimated Market Size ($B)": trend["values"]}, index=trend["years"])
    st.subheader("Market Trends")
    st.area_chart(chart_df)

    st.subheader("Competitor Landscape")
    for comp in get_competitors():
        with st.container(border=True):
            st.write(f"**{comp['name']}**")
            x, y, z = st.columns(3)
            x.metric("Market Share", f"{comp['market_share']}%")
            y.metric("Revenue", comp["revenue"])
            z.metric("Growth", comp["growth"])
            st.progress(comp["market_share"] / 100)

# ---------- Milestone 2: Risk + SWOT ----------
with tabs[2]:
    st.header("Milestone 2 â€” Risk Assessment & SWOT Analysis")
    project = st.session_state.get("selected_project")
    if project is None and projects:
        project = project_dict(projects[0])
        st.session_state["selected_project"] = project

    if project:
        st.caption(f"Analyzing PostgreSQL project: **{project['project_name']}**")

    c1, c2 = st.columns(2)
    with c1:
        market_competition = st.selectbox(
            "Market Competition", ["Low", "Medium", "High"],
            index=project_competition_default(project),
        )
        team_expertise = st.selectbox("Team Expertise", ["Low", "Medium", "High"], index=1)
        resource_availability = st.selectbox(
            "Resource Availability", ["Limited", "Moderate", "Good"],
            index=project_resource_default(project),
        )
    with c2:
        innovation_level = st.selectbox("Innovation Level", ["Low", "Medium", "High"], index=1)
        market_research = st.selectbox("Market Research", ["Limited", "Moderate", "Strong"], index=1)

    st.divider()
    st.subheader("Project Feasibility")
    f1, f2 = st.columns(2)
    with f1:
        market_opportunity = st.slider("Market Opportunity", 0, 100, 64)
        team_capability = st.slider("Team Capability", 0, 100, 64)
    with f2:
        competitive_advantage = st.slider("Competitive Advantage", 0, 100, 64)
        resource_score = st.slider("Resource Availability", 0, 100, 64)

    inputs = {
        "risk": {
            "market_competition": market_competition,
            "team_expertise": team_expertise,
            "resource_availability": resource_availability,
            "innovation_level": innovation_level,
            "market_research": market_research,
        },
        "feasibility": {
            "market_opportunity": market_opportunity,
            "team_capability": team_capability,
            "competitive_advantage": competitive_advantage,
            "resource_availability": resource_score,
        },
    }

    if st.button("Calculate Risk, SWOT & Feasibility", type="primary", use_container_width=True):
        st.session_state["milestone2_result"] = run_assessment(inputs)
        st.session_state.pop("ai_recommendation", None)

    result = st.session_state.get("milestone2_result")
    if result:
        st.divider()
        st.subheader("Risk Score & Breakdown")
        cols = st.columns(5)
        for col, (label, value) in zip(cols, result["breakdown"].items()):
            col.metric(label, f"{value}/5")

        a, b, c = st.columns(3)
        a.metric("Overall Risk Score", f"{result['risk_score']}/100")
        b.metric("Risk Status", result["risk_status"])
        c.metric("Success Probability", f"{result['success_probability']}%")
        st.progress(result["risk_score"] / 100)

        st.subheader("SWOT Analysis")
        display_swot(result["swot"])

        st.subheader("Project Feasibility")
        a, b = st.columns([1, 2])
        a.metric("Feasibility Score", f"{result['feasibility_score']}%")
        b.progress(result["feasibility_score"] / 100)
        st.info(result["feasibility_label"])
    else:
        st.info("Choose the assessment inputs and click **Calculate Risk, SWOT & Feasibility**.")

# ---------- Milestone 2: AI Recommendations ----------
with tabs[3]:
    st.header("Milestone 2 â€” Recommendations")
    project = st.session_state.get("selected_project")
    result = st.session_state.get("milestone2_result")

    if not result:
        st.info("Complete the Risk & SWOT assessment first.")
    else:
        score = result["feasibility_score"]
        risk = result["risk_score"]
        if score >= 60 and risk < 70:
            recommendation = "Feasible"
            message = "The project is feasible but has some risks. Review the weaknesses and threats."
        elif score >= 50 and risk < 85:
            recommendation = "Conditionally Feasible"
            message = "The project shows potential, but risk-reduction actions should be completed before major investment."
        else:
            recommendation = "Needs Improvement"
            message = "The project currently has significant risk or feasibility gaps. Strengthen weak areas before proceeding."

        st.info(f"## {recommendation}")
        st.write(message)
        st.divider()
        st.subheader("Assessment Summary")
        a, b, c, d = st.columns(4)
        a.metric("Feasibility", f"{score}%")
        b.metric("Risk", result["risk_status"])
        c.metric("Success Probability", f"{result['success_probability']}%")
        d.metric("SWOT Factors", sum(len(v) for v in result["swot"].values()))

        st.subheader("ðŸ¤– Groq AI Recommendation")
        st.caption("Groq only explains the calculated results; it does not replace the deterministic risk/SWOT/feasibility engines.")
        if st.button("Generate AI Recommendations", type="primary"):
            with st.spinner("Generating recommendations with Groq..."):
                ai_text, ai_error = groq_recommendation(project, result)
            if ai_text:
                st.session_state["ai_recommendation"] = ai_text
            else:
                st.error(ai_error)
        if st.session_state.get("ai_recommendation"):
            st.markdown(st.session_state["ai_recommendation"])

# ---------- Combined Final Dashboard ----------
with tabs[4]:
    st.header("Final ML Market Intelligence Dashboard")
    project = st.session_state.get("selected_project")
    result = st.session_state.get("milestone2_result")

    if project:
        st.subheader("Project Submission")
        show_project_card(project)
    else:
        st.info("Add or select a project from Milestone 1 first.")

    st.divider()
    st.subheader("Integrated Results")
    if result:
        a, b, c, d = st.columns(4)
        a.metric("Risk Score", f"{result['risk_score']}/100")
        b.metric("Risk Status", result["risk_status"])
        c.metric("Success Probability", f"{result['success_probability']}%")
        d.metric("Feasibility", f"{result['feasibility_score']}%")
    else:
        st.info("Run Milestone 2 analysis to populate the integrated results.")

    st.divider()
    st.subheader("Market Analysis")
    market = get_market_size()
    a, b, c = st.columns(3)
    a.metric("TAM", market["tam"]["value"])
    b.metric("SAM", market["sam"]["value"])
    c.metric("SOM", market["som"]["value"])

    trend = get_market_trends()
    chart_df = pd.DataFrame({"Estimated Market Size ($B)": trend["values"]}, index=trend["years"])
    st.area_chart(chart_df)

    st.subheader("Competitor Landscape")
    comp_cols = st.columns(len(get_competitors()))
    for col, comp in zip(comp_cols, get_competitors()):
        with col:
            st.write(f"**{comp['name']}**")
            st.metric("Market Share", f"{comp['market_share']}%")
            st.caption(f"Revenue: {comp['revenue']}")
            st.caption(f"Growth: {comp['growth']}")
            st.progress(comp["market_share"] / 100)

    if st.session_state.get("ai_recommendation"):
        st.divider()
        st.subheader("AI Recommendation")
        st.markdown(st.session_state["ai_recommendation"])




