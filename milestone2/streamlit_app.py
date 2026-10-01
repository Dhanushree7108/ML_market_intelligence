"""Streamlit implementation of Milestone 2 and AI-assisted recommendations."""

import os

import pandas as pd
import streamlit as st

from database import fetch_projects, insert_project
from risk_engine import calculate_risk, calculate_success_probability, get_risk_status, risk_breakdown
from swot_analysis import generate_swot
from feasibility import calculate_feasibility, feasibility_label
from market_analysis import get_market_size, get_market_trends, get_competitors

st.set_page_config(page_title="Prediction AI", page_icon="ðŸ“Š", layout="wide")


def _groq_key():
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    try:
        return st.secrets.get("GROQ_API_KEY")
    except Exception:
        return None


def generate_ai_recommendation(project, result):
    """Generate an AI explanation while keeping the deterministic scoring intact."""
    key = _groq_key()
    if not key:
        return None, "GROQ_API_KEY is not configured. Add it to your local .env or Streamlit Cloud Secrets."

    try:
        from groq import Groq

        client = Groq(api_key=key)
        project_name = project.get("project_name", "Project") if project else "Project"
        prompt = f"""
You are an AI business analyst supporting a student ML Market Intelligence project.
Give a concise, practical recommendation based ONLY on the supplied project assessment.
Do not invent market facts, competitors, financial figures, or statistics.

Project: {project_name}
Target market: {project.get('target_market', 'Not provided') if project else 'Not provided'}
Description: {project.get('project_description', 'Not provided') if project else 'Not provided'}
Budget: {project.get('budget', 'Not provided') if project else 'Not provided'}

Risk score: {result['risk_score']}/100
Risk status: {result['risk_status']}
Success probability: {result['success_probability']}%
Feasibility: {result['feasibility_score']}% ({result['feasibility_label']})
SWOT: {result['swot']}

Return exactly these sections:
1. Executive assessment
2. Top 3 actions to reduce risk
3. How to strengthen feasibility
4. How to use strengths/opportunities
5. Key risks to monitor
Keep the answer under 450 words.
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


def load_projects():
    try:
        return fetch_projects(), None
    except Exception as exc:
        return [], str(exc)


def project_dict(row):
    return {
        "id": row[0], "project_name": row[1], "project_description": row[2],
        "target_market": row[3], "budget": row[4], "competition": row[5] or "",
        "resources": row[6] or "", "objectives": row[7] or "", "created_at": row[8],
    }


def run_assessment(inputs):
    risk_score = calculate_risk(**inputs["risk"])
    swot = generate_swot(
        inputs["risk"]["team_expertise"], inputs["risk"]["innovation_level"],
        inputs["risk"]["market_competition"], inputs["risk"]["resource_availability"],
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


st.title("Prediction AI")
st.subheader("Risk Assessment, SWOT Analysis & AI Recommendations")
st.caption("Milestone 2 â€¢ Streamlit â€¢ Rule-based scoring + Groq AI")
st.divider()

tabs = st.tabs(["Project Input", "Risk Assessment", "Recommendations", "Dashboard"])
projects, db_error = load_projects()

with tabs[0]:
    st.header("Project Input")
    if db_error:
        st.warning("PostgreSQL could not be reached. You can still run the assessment controls.")
        with st.expander("Database error details"):
            st.code(db_error)

    selected = None
    if projects:
        labels = [f"{r[1]} â€” {r[3]} â€” â‚¹{float(r[4]):,.2f}" for r in projects]
        selected_index = st.selectbox("Select Milestone 1 Project", range(len(labels)), format_func=lambda i: labels[i])
        selected = project_dict(projects[selected_index])
        st.session_state["selected_project"] = selected
        c1, c2, c3 = st.columns(3)
        c1.write(f"**Project**\n\n{selected['project_name']}")
        c2.write(f"**Target Market**\n\n{selected['target_market']}")
        c3.write(f"**Budget**\n\nâ‚¹{float(selected['budget']):,.2f}")
        st.write(f"**Description**\n\n{selected['project_description']}")
    else:
        st.info("No Milestone 1 project found. You can add one below when PostgreSQL is available.")
        with st.form("project_form"):
            name = st.text_input("Startup / Project Name *")
            target_market = st.text_input("Target Market *")
            budget = st.number_input("Budget (â‚¹)", min_value=0.0, step=1000.0)
            description = st.text_area("Project Description *")
            competition = st.text_input("Competition")
            resources = st.text_input("Resources")
            objectives = st.text_area("Objectives")
            save = st.form_submit_button("Save Project", type="primary")
            if save:
                if not name or not target_market or not description:
                    st.error("Please fill the required fields.")
                else:
                    try:
                        new_id = insert_project(name, description, target_market, budget, competition, resources, objectives)
                        st.success(f"Project saved successfully (ID {new_id}).")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not save project: {exc}")

with tabs[1]:
    st.header("Risk Assessment Inputs")
    c1, c2 = st.columns(2)
    with c1:
        market_competition = st.selectbox("Market Competition", ["Low", "Medium", "High"], index=0)
        team_expertise = st.selectbox("Team Expertise", ["Low", "Medium", "High"], index=0)
        resource_availability = st.selectbox("Resource Availability", ["Limited", "Moderate", "Good"], index=0)
    with c2:
        innovation_level = st.selectbox("Innovation Level", ["Low", "Medium", "High"], index=0)
        market_research = st.selectbox("Market Research", ["Limited", "Moderate", "Strong"], index=0)

    st.divider()
    st.header("Project Feasibility")
    f1, f2 = st.columns(2)
    with f1:
        market_opportunity = st.slider("Market Opportunity", 0, 100, 60)
        team_capability = st.slider("Team Capability", 0, 100, 60)
    with f2:
        competitive_advantage = st.slider("Competitive Advantage", 0, 100, 60)
        resource_score = st.slider("Resource Availability", 0, 100, 60)

    inputs = {
        "risk": {
            "market_competition": market_competition, "team_expertise": team_expertise,
            "resource_availability": resource_availability, "innovation_level": innovation_level,
            "market_research": market_research,
        },
        "feasibility": {
            "market_opportunity": market_opportunity, "team_capability": team_capability,
            "competitive_advantage": competitive_advantage, "resource_availability": resource_score,
        },
    }
    if st.button("Calculate Risk & SWOT", type="primary", use_container_width=True):
        st.session_state["milestone2_result"] = run_assessment(inputs)

    result = st.session_state.get("milestone2_result")
    if result:
        st.divider()
        st.header("Risk Score & Breakdown")
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
        st.metric("Feasibility Score", f"{result['feasibility_score']}%")
        st.progress(result["feasibility_score"] / 100)
        st.write(result["feasibility_label"])

with tabs[2]:
    st.header("Final Recommendation")
    result = st.session_state.get("milestone2_result")
    project = st.session_state.get("selected_project")
    if not result:
        st.info("Complete the Risk Assessment first to generate recommendations.")
    else:
        score, risk = result["feasibility_score"], result["risk_score"]
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
        st.subheader("AI-Powered Recommendations â€” Groq")
        if st.button("Generate AI Recommendations", type="primary"):
            with st.spinner("Generating AI recommendations..."):
                ai_text, ai_error = generate_ai_recommendation(project, result)
            if ai_text:
                st.session_state["ai_recommendation"] = ai_text
            else:
                st.error(ai_error)
        if st.session_state.get("ai_recommendation"):
            st.markdown(st.session_state["ai_recommendation"])
        st.caption("The rule-based risk, SWOT and feasibility calculations remain deterministic; Groq adds the natural-language recommendation layer.")

with tabs[3]:
    st.header("Final Project Dashboard")
    project = st.session_state.get("selected_project")
    if project is None and projects:
        project = project_dict(projects[0])
    p1, p2, p3 = st.columns(3)
    with p1:
        st.subheader("Project")
        if project:
            st.write(f"**Name:** {project['project_name']}")
            st.write(f"**Target Market:** {project['target_market']}")
            st.write(f"**Budget:** â‚¹{float(project['budget']):,.2f}")
            st.write(f"**Description:** {project['project_description']}")
        else:
            st.info("No project submitted yet.")
    with p2:
        st.subheader("Market Analysis")
        market = get_market_size()
        a, b, c = st.columns(3)
        a.metric("TAM", market["tam"]["value"])
        b.metric("SAM", market["sam"]["value"])
        c.metric("SOM", market["som"]["value"])
        trend = get_market_trends()
        chart_df = pd.DataFrame({"Estimated Market Size ($B)": trend["values"]}, index=trend["years"])
        st.area_chart(chart_df)
    with p3:
        st.subheader("Competitor Landscape")
        for comp in get_competitors():
            st.write(f"**{comp['name']}**")
            x, y, z = st.columns(3)
            x.caption(f"Market Share\n{comp['market_share']}%")
            y.caption(f"Revenue\n{comp['revenue']}")
            z.caption(f"Growth\n{comp['growth']}")
            st.progress(comp["market_share"] / 100)

    result = st.session_state.get("milestone2_result")
    if result:
        st.divider()
        st.subheader("Milestone 2 Summary")
        a, b, c, d = st.columns(4)
        a.metric("Risk Score", f"{result['risk_score']}/100")
        b.metric("Risk Status", result["risk_status"])
        c.metric("Success Probability", f"{result['success_probability']}%")
        d.metric("Feasibility", f"{result['feasibility_score']}%")
        if st.session_state.get("ai_recommendation"):
            st.divider()
            st.subheader("AI Recommendation Summary")
            st.markdown(st.session_state["ai_recommendation"])

