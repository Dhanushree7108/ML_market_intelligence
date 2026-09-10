"""Streamlit implementation of Milestone 2.

Only this milestone is implemented here. It reads Milestone 1 project data
from the existing PostgreSQL `projects` table and provides:
Project Input -> Risk Assessment -> Recommendations -> Dashboard.
"""

import streamlit as st
import pandas as pd

from database import fetch_projects, insert_project
from risk_engine import (
    calculate_risk,
    calculate_success_probability,
    get_risk_status,
    risk_breakdown,
)
from swot_analysis import generate_swot
from feasibility import calculate_feasibility, feasibility_label
from market_analysis import get_market_size, get_market_trends, get_competitors


st.set_page_config(
    page_title="Prediction AI",
    page_icon="📊",
    layout="wide",
)


# ---------- helpers ----------
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


def display_swot(swot):
    left, right = st.columns(2)

    with left:
        st.markdown("### Strengths")
        if swot["Strengths"]:
            for item in swot["Strengths"]:
                st.success(f"• {item}")
        else:
            st.info("No strength rule was triggered by the selected inputs.")

        st.markdown("### Opportunities")
        for item in swot["Opportunities"]:
            st.info(f"• {item}")

    with right:
        st.markdown("### Weaknesses")
        if swot["Weaknesses"]:
            for item in swot["Weaknesses"]:
                st.warning(f"• {item}")
        else:
            st.info("No weakness rule was triggered by the selected inputs.")

        st.markdown("### Threats")
        for item in swot["Threats"]:
            st.error(f"• {item}")


# ---------- header ----------
st.title("Prediction AI")
st.subheader("Risk Assessment & SWOT Analysis")
st.caption("AI-powered risk scoring and strategic evaluation")
st.divider()

tabs = st.tabs(["Project Input", "Risk Assessment", "Recommendations", "Dashboard"])


# ---------- Project Input ----------
projects, db_error = load_projects()

with tabs[0]:
    st.header("Project Input")
    st.write("Enter the details of the startup project.")

    if db_error:
        st.warning(
            "PostgreSQL could not be reached. Milestone 2 can still be demonstrated "
            "with the assessment controls, but project data cannot be loaded."
        )
        with st.expander("Database error details"):
            st.code(db_error)

    selected = None
    if projects:
        labels = [
            f"{r[1]}  —  {r[3]}  —  ₹{float(r[4]):,.2f}"
            for r in projects
        ]
        selected_index = st.selectbox(
            "Select Milestone 1 Project",
            range(len(labels)),
            format_func=lambda i: labels[i],
        )
        selected = project_dict(projects[selected_index])
        st.session_state["selected_project"] = selected

        st.markdown("#### Selected project")
        c1, c2, c3 = st.columns(3)
        c1.write(f"**Startup / Project Name**\n\n{selected['project_name']}")
        c2.write(f"**Target Market**\n\n{selected['target_market']}")
        c3.write(f"**Budget**\n\n₹{float(selected['budget']):,.2f}")
        st.write(f"**Project Description**\n\n{selected['project_description']}")
        if selected["competition"] or selected["resources"] or selected["objectives"]:
            a, b, c = st.columns(3)
            a.write(f"**Competition**\n\n{selected['competition'] or 'Not provided'}")
            b.write(f"**Resources**\n\n{selected['resources'] or 'Not provided'}")
            c.write(f"**Objectives**\n\n{selected['objectives'] or 'Not provided'}")
    else:
        st.info("No Milestone 1 project found. You can add a project below.")
        with st.form("project_form"):
            name = st.text_input("Startup Name *")
            industry = st.text_input("Industry")
            business_model = st.text_input("Business Model")
            target_market = st.text_input("Target Market *")
            budget = st.number_input("Budget (₹)", min_value=0.0, step=1000.0)
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
                        new_id = insert_project(
                            name,
                            description,
                            target_market,
                            budget,
                            competition,
                            resources,
                            objectives,
                        )
                        st.success(f"Project saved successfully (ID {new_id}).")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not save project: {exc}")

    st.caption(
        "Industry and Business Model are presentation fields; the existing "
        "Milestone 1 database schema is not changed by Milestone 2."
    )


# ---------- Risk Assessment ----------
with tabs[1]:
    st.header("Risk Assessment Inputs")

    c1, c2 = st.columns(2)
    with c1:
        market_competition = st.selectbox(
            "Market Competition", ["Low", "Medium", "High"], index=0
        )
        team_expertise = st.selectbox(
            "Team Expertise", ["Low", "Medium", "High"], index=0
        )
        resource_availability = st.selectbox(
            "Resource Availability", ["Limited", "Moderate", "Good"], index=0
        )
    with c2:
        innovation_level = st.selectbox(
            "Innovation Level", ["Low", "Medium", "High"], index=0
        )
        market_research = st.selectbox(
            "Market Research", ["Limited", "Moderate", "Strong"], index=0
        )

    st.divider()
    st.header("Project Feasibility")
    st.caption("Each feasibility factor is scored from 0 to 100.")

    f1, f2 = st.columns(2)
    with f1:
        market_opportunity = st.slider("Market Opportunity", 0, 100, 60)
        team_capability = st.slider("Team Capability", 0, 100, 60)
    with f2:
        competitive_advantage = st.slider("Competitive Advantage", 0, 100, 60)
        resource_score = st.slider("Resource Availability", 0, 100, 60)

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

    if st.button("Calculate Risk & SWOT", type="primary", use_container_width=True):
        st.session_state["milestone2_result"] = run_assessment(inputs)

    result = st.session_state.get("milestone2_result")
    if result:
        st.divider()
        st.header("Risk Score & Breakdown")

        b = result["breakdown"]
        cols = st.columns(5)
        for col, (label, value) in zip(cols, b.items()):
            col.metric(label, f"{value}/5")

        st.divider()
        r1, r2 = st.columns([1, 2])
        with r1:
            st.metric("Overall Risk Score", f"{result['risk_score']}/100")
        with r2:
            status = result["risk_status"]
            if status == "HIGH RISK":
                st.error(status)
            elif status == "MEDIUM RISK":
                st.warning(status)
            else:
                st.success(status)

        st.write("**Overall Risk**")
        st.progress(result["risk_score"] / 100)

        st.subheader("Success Probability")
        st.progress(result["success_probability"] / 100)
        st.write(f"{result['success_probability']}%")

        st.header("SWOT Analysis")
        display_swot(result["swot"])

        st.header("Project Feasibility")
        st.metric("Feasibility Score", f"{result['feasibility_score']}%")
        st.progress(result["feasibility_score"] / 100)
        st.write(result["feasibility_label"])
    else:
        st.info("Select the assessment inputs and click **Calculate Risk & SWOT**.")


# ---------- Recommendations ----------
with tabs[2]:
    st.header("Final Recommendation")
    result = st.session_state.get("milestone2_result")

    if not result:
        st.info("Complete the Risk Assessment first to generate the recommendation.")
    else:
        score = result["feasibility_score"]
        risk = result["risk_score"]

        if score >= 60 and risk < 70:
            recommendation = "Feasible"
            message = (
                "The project is feasible but has some risks. Please review the "
                "Weaknesses and Threats in the SWOT analysis."
            )
        elif score >= 50 and risk < 85:
            recommendation = "Conditionally Feasible"
            message = (
                "The project shows potential, but risk-reduction actions should "
                "be completed before major investment."
            )
        else:
            recommendation = "Needs Improvement"
            message = (
                "The project currently has significant risk or feasibility gaps. "
                "Strengthen the weak areas before proceeding."
            )

        st.info(f"## {recommendation}")
        st.write(message)

        st.divider()
        st.subheader("Key Factors Driving This Recommendation")
        swot = result["swot"]
        st.markdown(f"- **Feasibility Score:** {score}%")
        st.markdown(
            f"- **Overall Risk:** {result['risk_status']} "
            f"({risk}/100)"
        )
        st.markdown(
            f"- **Key Strengths/Opportunities:** "
            f"{len(swot['Strengths']) + len(swot['Opportunities'])} factors"
        )
        st.markdown(
            f"- **Key Weaknesses/Threats:** "
            f"{len(swot['Weaknesses']) + len(swot['Threats'])} factors"
        )


# ---------- Dashboard ----------
with tabs[3]:
    st.header("Project Submission")
    project = st.session_state.get("selected_project")

    if project is None and projects:
        project = project_dict(projects[0])

    p1, p2, p3 = st.columns(3)
    with p1:
        st.subheader("Latest Project")
        if project:
            st.write(f"**Startup / Project Name**\n\n{project['project_name']}")
            st.write(f"**Target Market**\n\n{project['target_market']}")
            st.write(f"**Budget**\n\n₹{float(project['budget']):,.2f}")
            st.write(
                f"**Project Description**\n\n"
                f"{project['project_description']}"
            )
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
        chart_df = pd.DataFrame(
            {"Estimated Market Size ($B)": trend["values"]},
            index=trend["years"],
        )
        st.caption("Market Trends (2020–2026)")
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
