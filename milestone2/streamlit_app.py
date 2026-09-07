"""Streamlit UI for Milestone 2: Risk Assessment & SWOT Analysis.

Milestone 2 follows the supplied plan: risk inputs are selected, a rule-based
risk score and success probability are calculated, SWOT is generated, and
project feasibility is calculated from four 0-100 inputs.
"""

import streamlit as st
from database import get_connection
from risk_engine import calculate_risk, get_risk_status, calculate_success_probability
from swot_analysis import generate_swot
from feasibility import calculate_feasibility

st.set_page_config(
    page_title="ML Market Intelligence - Milestone 2",
    page_icon="📊",
    layout="wide",
)


def latest_project():
    """Read the latest Milestone 1 project from PostgreSQL."""
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, project_name, project_description, target_market, budget,
                   competition, resources, objectives
            FROM projects ORDER BY id DESC LIMIT 1
            """
        )
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        if not row:
            return None
        return {
            "id": row[0],
            "project_name": row[1],
            "project_description": row[2],
            "target_market": row[3],
            "budget": row[4],
            "competition": row[5],
            "resources": row[6],
            "objectives": row[7],
        }
    except Exception as exc:
        st.warning(f"Could not load the latest project from PostgreSQL: {exc}")
        return None


st.title("Risk Assessment & SWOT Analysis")
st.caption("Milestone 2 • Risk Scoring • SWOT Analysis • Project Feasibility")

project = latest_project()

if project:
    with st.expander("Milestone 1 Project Data", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.write(f"**Project:** {project['project_name']}")
        c2.write(f"**Target Market:** {project['target_market']}")
        c3.write(f"**Budget:** {project['budget']}")
        st.write(f"**Description:** {project['project_description']}")
else:
    st.info("No project was found in PostgreSQL. You can still demonstrate Milestone 2 using the default inputs.")

st.divider()

st.subheader("1. Risk Assessment Inputs")

c1, c2 = st.columns(2)
with c1:
    market_competition = st.selectbox(
        "Market Competition",
        ["High", "Medium", "Low"],
        index=1,
    )
    team_expertise = st.selectbox(
        "Team Expertise",
        ["Low", "Medium", "High"],
        index=1,
    )
    resource_availability = st.selectbox(
        "Resource Availability",
        ["Limited", "Moderate", "Good"],
        index=1,
    )
with c2:
    innovation_level = st.selectbox(
        "Innovation Level",
        ["Low", "Medium", "High"],
        index=1,
    )
    market_research = st.selectbox(
        "Market Research",
        ["Limited", "Moderate", "Strong"],
        index=1,
    )

st.subheader("2. Project Feasibility")
st.caption("Adjust the four inputs from 0 to 100. The feasibility score is their average.")

f1, f2 = st.columns(2)
with f1:
    market_opportunity = st.slider("Market Opportunity", 0, 100, 50)
    team_capability = st.slider("Team Capability", 0, 100, 50)
with f2:
    competitive_advantage = st.slider("Competitive Advantage", 0, 100, 50)
    resource_score = st.slider("Resource Availability", 0, 100, 50)

if st.button("Calculate Risk & SWOT", type="primary", use_container_width=True):
    risk_score = calculate_risk(
        market_competition=market_competition,
        team_expertise=team_expertise,
        resource_availability=resource_availability,
        innovation_level=innovation_level,
        market_research=market_research,
    )
    risk_status = get_risk_status(risk_score)
    success_probability = calculate_success_probability(risk_score)
    swot = generate_swot(
        team_expertise,
        innovation_level,
        market_competition,
        resource_availability,
        market_research,
    )
    feasibility_score = calculate_feasibility(
        market_opportunity,
        team_capability,
        competitive_advantage,
        resource_score,
    )

    st.session_state["milestone2_result"] = {
        "risk_score": risk_score,
        "risk_status": risk_status,
        "success_probability": success_probability,
        "swot": swot,
        "feasibility_score": feasibility_score,
    }

result = st.session_state.get("milestone2_result")

if result:
    st.divider()
    st.subheader("3. Risk & Feasibility Results")

    m1, m2, m3 = st.columns(3)
    m1.metric("Risk Score", f"{result['risk_score']}/100")
    m2.metric("Risk Status", result["risk_status"])
    m3.metric("Success Probability", f"{result['success_probability']}%")

    st.write("**Risk Score Progress**")
    st.progress(result["risk_score"] / 100)

    st.write("**Feasibility Score**")
    st.progress(result["feasibility_score"] / 100)
    st.metric("Project Feasibility", f"{result['feasibility_score']}/100")

    st.subheader("4. SWOT Analysis")
    swot = result["swot"]
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("### 💪 Strengths")
        for item in swot["Strengths"]:
            st.success(item)
        st.markdown("### ⚠️ Weaknesses")
        for item in swot["Weaknesses"]:
            st.warning(item)
    with s2:
        st.markdown("### 🚀 Opportunities")
        for item in swot["Opportunities"]:
            st.info(item)
        st.markdown("### 🛡️ Threats")
        for item in swot["Threats"]:
            st.error(item)
else:
    st.info("Set the Milestone 2 inputs above and click **Calculate Risk & SWOT** to generate the results.")

st.divider()
st.caption("Milestone 3 AI recommendations and LangGraph are not included in this Milestone 2 implementation.")
