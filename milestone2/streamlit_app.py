"""
Prediction AI - Milestone 3

Milestone 2:
- Project Input
- Risk Assessment
- SWOT Analysis
- Feasibility Analysis
- Market Analysis
- Competitor Analysis
- Dashboard

Milestone 3:
- AI Recommendations
- Recommendation Priority
- Risk Mitigation
- Strategic Reasoning
- LangGraph Agent Workflow
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

from feasibility import (
    calculate_feasibility,
    feasibility_label,
)

from market_analysis import (
    get_market_size,
    get_market_trends,
    get_competitors,
)

from recommendation_engine import (
    generate_recommendations,
    generate_risk_mitigations,
    get_priority_style,
    get_impact_style,
)

from langgraph_workflow import run_langgraph_workflow


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Prediction AI",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# CLEAN CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F4F7FC;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }

    /* Reduce Streamlit vertical gaps */
    div[data-testid="stVerticalBlock"] {
        gap: 0.45rem;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 0.8rem;
    }

    h1 {
        color: #0B1220 !important;
        font-weight: 750 !important;
    }

    h2 {
        color: #111C33 !important;
        font-weight: 700 !important;
    }

    h3 {
        color: #111C33 !important;
        font-weight: 700 !important;
    }

    p {
        color: #475569;
    }

    /* Tabs */

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: white;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #DCE3EF;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 7px;
        font-weight: 600;
    }

    /* Metrics */

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #DCE3EF;
        border-radius: 10px;
        padding: 14px;
    }

    div[data-testid="stMetricValue"] {
        color: #0B1220 !important;
    }

    /* Buttons */

    .stButton > button {
        border-radius: 8px !important;
        font-weight: 650 !important;
    }

    /* Small AI badge */

    .ai-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        background: #EEF2FF;
        color: #4338CA;
        border: 1px solid #C7D2FE;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNCTIONS
# ============================================================

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

    risk_score = calculate_risk(
        **inputs["risk"]
    )

    swot = generate_swot(
        inputs["risk"]["team_expertise"],
        inputs["risk"]["innovation_level"],
        inputs["risk"]["market_competition"],
        inputs["risk"]["resource_availability"],
        inputs["risk"]["market_research"],
    )

    feasibility = calculate_feasibility(
        **inputs["feasibility"]
    )

    return {
        "risk_score": risk_score,
        "risk_status": get_risk_status(risk_score),
        "success_probability": calculate_success_probability(
            risk_score
        ),
        "breakdown": risk_breakdown(
            **inputs["risk"]
        ),
        "swot": swot,
        "feasibility_score": feasibility,
        "feasibility_label": feasibility_label(
            feasibility
        ),
        "inputs": inputs,
    }


def display_swot(swot):

    left, right = st.columns(2)

    with left:

        st.subheader("💪 Strengths")

        if swot["Strengths"]:
            for item in swot["Strengths"]:
                st.success(item)
        else:
            st.info("No strength rule was triggered.")

        st.subheader("🚀 Opportunities")

        for item in swot["Opportunities"]:
            st.info(item)

    with right:

        st.subheader("⚠️ Weaknesses")

        if swot["Weaknesses"]:
            for item in swot["Weaknesses"]:
                st.warning(item)
        else:
            st.info("No weakness rule was triggered.")

        st.subheader("🛡️ Threats")

        for item in swot["Threats"]:
            st.error(item)


# ============================================================
# HEADER
# ============================================================

st.title("Prediction AI")

st.subheader(
    "Risk Assessment, Recommendations & Strategic Reasoning"
)

st.caption(
    "AI-powered risk scoring, SWOT analysis, feasibility "
    "evaluation, market intelligence and strategic recommendations"
)

st.divider()


# ============================================================
# LOAD DATABASE
# ============================================================

projects, db_error = load_projects()


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📁 Project Input",
        "⚠️ Risk Assessment",
        "🤖 Recommendations",
        "📊 Dashboard",
    ]
)


# ============================================================
# TAB 1 — PROJECT INPUT
# ============================================================

with tab1:

    st.header("Project Input")

    st.write(
        "Select the project created during Milestone 1 "
        "or create a new project."
    )

    if db_error:

        st.warning(
            "PostgreSQL could not be reached. "
            "Project records cannot be loaded."
        )

        with st.expander("Database Error"):
            st.code(db_error)

    if projects:

        labels = [
            f"{row[1]} — {row[3]} — ₹{float(row[4]):,.2f}"
            for row in projects
        ]

        selected_index = st.selectbox(
            "Select Milestone 1 Project",
            range(len(labels)),
            format_func=lambda i: labels[i],
        )

        selected = project_dict(
            projects[selected_index]
        )

        st.session_state["selected_project"] = selected

        st.subheader("Selected Project")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.write("**Project Name**")
            st.write(selected["project_name"])

        with c2:
            st.write("**Target Market**")
            st.write(selected["target_market"])

        with c3:
            st.write("**Budget**")
            st.write(
                f"₹{float(selected['budget']):,.2f}"
            )

        st.write("**Project Description**")
        st.write(selected["project_description"])

        st.divider()

        x, y, z = st.columns(3)

        with x:
            st.write("**Competition**")
            st.write(
                selected["competition"] or "Not provided"
            )

        with y:
            st.write("**Resources**")
            st.write(
                selected["resources"] or "Not provided"
            )

        with z:
            st.write("**Objectives**")
            st.write(
                selected["objectives"] or "Not provided"
            )

    else:

        st.info("No Milestone 1 project found.")

        with st.form("project_form"):

            name = st.text_input("Startup Name *")

            target_market = st.text_input(
                "Target Market *"
            )

            budget = st.number_input(
                "Budget (₹)",
                min_value=0.0,
                step=1000.0,
            )

            description = st.text_area(
                "Project Description *"
            )

            competition = st.text_input(
                "Competition"
            )

            resources = st.text_input(
                "Resources"
            )

            objectives = st.text_area(
                "Objectives"
            )

            save = st.form_submit_button(
                "Save Project"
            )

            if save:

                if (
                    not name
                    or not target_market
                    or not description
                ):

                    st.error(
                        "Please fill all required fields."
                    )

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

                        st.success(
                            f"Project saved successfully. ID: {new_id}"
                        )

                        st.rerun()

                    except Exception as exc:

                        st.error(
                            f"Could not save project: {exc}"
                        )


# ============================================================
# TAB 2 — RISK ASSESSMENT
# ============================================================

with tab2:

    st.header("Risk Assessment")

    st.write(
        "Evaluate market, team, innovation, resources "
        "and research factors."
    )

    left, right = st.columns(2)

    with left:

        market_competition = st.selectbox(
            "Market Competition",
            ["Low", "Medium", "High"],
        )

        team_expertise = st.selectbox(
            "Team Expertise",
            ["Low", "Medium", "High"],
        )

        resource_availability = st.selectbox(
            "Resource Availability",
            ["Limited", "Moderate", "Good"],
        )

    with right:

        innovation_level = st.selectbox(
            "Innovation Level",
            ["Low", "Medium", "High"],
        )

        market_research = st.selectbox(
            "Market Research",
            ["Limited", "Moderate", "Strong"],
        )

    st.divider()

    st.header("Project Feasibility")

    f1, f2 = st.columns(2)

    with f1:

        market_opportunity = st.slider(
            "Market Opportunity",
            0,
            100,
            60,
        )

        team_capability = st.slider(
            "Team Capability",
            0,
            100,
            60,
        )

    with f2:

        competitive_advantage = st.slider(
            "Competitive Advantage",
            0,
            100,
            60,
        )

        resource_score = st.slider(
            "Resource Availability Score",
            0,
            100,
            60,
        )

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

    if st.button(
        "Calculate Risk & SWOT",
        type="primary",
        use_container_width=True,
    ):

        st.session_state["milestone2_result"] = (
            run_assessment(inputs)
        )

        st.success(
            "Risk assessment completed successfully."
        )

    result = st.session_state.get(
        "milestone2_result"
    )

    if result:

        st.divider()

        st.subheader("Risk Score")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Overall Risk",
                f"{result['risk_score']}/100",
            )

        with c2:
            st.metric(
                "Risk Status",
                result["risk_status"],
            )

        with c3:
            st.metric(
                "Success Probability",
                f"{result['success_probability']}%",
            )

        st.progress(
            min(
                max(
                    result["risk_score"] / 100,
                    0,
                ),
                1,
            )
        )

        st.subheader("Risk Breakdown")

        breakdown = result["breakdown"]

        cols = st.columns(len(breakdown))

        for col, (label, value) in zip(
            cols,
            breakdown.items(),
        ):

            col.metric(
                label,
                f"{value}/5",
            )

        st.divider()

        st.subheader("SWOT Analysis")

        display_swot(
            result["swot"]
        )

        st.divider()

        st.subheader("Feasibility")

        st.metric(
            "Feasibility Score",
            f"{result['feasibility_score']}%",
        )

        st.progress(
            min(
                max(
                    result["feasibility_score"] / 100,
                    0,
                ),
                1,
            )
        )

        st.info(
            result["feasibility_label"]
        )

    else:

        st.info(
            "Complete the inputs and click "
            "**Calculate Risk & SWOT**."
        )


# ============================================================
# TAB 3 — MILESTONE 3
# ============================================================

with tab3:

    st.header(
        "Recommendations & Strategic Reasoning"
    )

    st.caption(
        "Convert assessment results into actionable "
        "strategic recommendations."
    )

    result = st.session_state.get(
        "milestone2_result"
    )

    if not result:

        st.warning(
            "Please complete Risk Assessment first."
        )

    else:

        project = st.session_state.get(
            "selected_project"
        )

        # ====================================================
        # ASSESSMENT SUMMARY
        # ====================================================

        st.subheader("Assessment Summary")

        a, b, c = st.columns(3)

        with a:
            st.metric(
                "Risk Score",
                f"{result['risk_score']}/100",
            )

        with b:
            st.metric(
                "Feasibility",
                f"{result['feasibility_score']}%",
            )

        with c:
            st.metric(
                "Success Probability",
                f"{result['success_probability']}%",
            )

        st.divider()

        # ====================================================
        # AI RECOMMENDATIONS
        # ====================================================

        st.subheader("🤖 AI Recommendations")

        st.markdown(
            '<div class="ai-badge">'
            '✨ AI POWERED • STRATEGIC REASONING'
            '</div>',
            unsafe_allow_html=True,
        )

        recommendations = generate_recommendations(
            risk_score=result["risk_score"],
            feasibility_score=result["feasibility_score"],
            project=project,
        )

        # Two compact columns
        for index in range(0, len(recommendations), 2):

            col1, col2 = st.columns(2, gap="small")

            recommendation_1 = recommendations[index]

            with col1:

                with st.container(border=True):

                    st.markdown(
                        f"### {recommendation_1['title']}"
                    )

                    st.caption(
                        f"{recommendation_1['category']}  •  "
                        f"{get_priority_style(recommendation_1['priority'])}"
                    )

                    st.write(
                        recommendation_1["description"]
                    )

                    st.info(
                        f"**Recommended Action:** "
                        f"{recommendation_1['action']}"
                    )

                    st.caption(
                        f"**Purpose:** "
                        f"{recommendation_1['purpose']}"
                    )

            if index + 1 < len(recommendations):

                recommendation_2 = recommendations[
                    index + 1
                ]

                with col2:

                    with st.container(border=True):

                        st.markdown(
                            f"### {recommendation_2['title']}"
                        )

                        st.caption(
                            f"{recommendation_2['category']}  •  "
                            f"{get_priority_style(recommendation_2['priority'])}"
                        )

                        st.write(
                            recommendation_2["description"]
                        )

                        st.info(
                            f"**Recommended Action:** "
                            f"{recommendation_2['action']}"
                        )

                        st.caption(
                            f"**Purpose:** "
                            f"{recommendation_2['purpose']}"
                        )

        st.divider()

        # ====================================================
        # RISK MITIGATION
        # ====================================================

        st.subheader("🛡️ Risk Mitigation")

        st.caption(
            "Identify risks and connect each risk "
            "to a practical mitigation strategy."
        )

        mitigations = generate_risk_mitigations(
            risk_score=result["risk_score"],
            feasibility_score=result["feasibility_score"],
        )

        category = st.radio(
            "Filter Risks",
            [
                "All Risks",
                "Financial",
                "Market",
                "Technical",
            ],
            horizontal=True,
        )

        if category == "All Risks":

            filtered = mitigations

        else:

            filtered = [
                item
                for item in mitigations
                if item["category"] == category
            ]

        for index in range(0, len(filtered), 2):

            col1, col2 = st.columns(2, gap="small")

            mitigation_1 = filtered[index]

            with col1:

                with st.container(border=True):

                    st.markdown(
                        f"### ⚠️ {mitigation_1['risk']}"
                    )

                    st.caption(
                        mitigation_1["category"]
                    )

                    st.markdown(
                        f"**Impact:** "
                        f"{get_impact_style(mitigation_1['impact'])}"
                    )

                    st.markdown(
                        f"**Mitigation Strategy:** "
                        f"{mitigation_1['strategy']}"
                    )

                    st.write(
                        mitigation_1["description"]
                    )

            if index + 1 < len(filtered):

                mitigation_2 = filtered[
                    index + 1
                ]

                with col2:

                    with st.container(border=True):

                        st.markdown(
                            f"### ⚠️ {mitigation_2['risk']}"
                        )

                        st.caption(
                            mitigation_2["category"]
                        )

                        st.markdown(
                            f"**Impact:** "
                            f"{get_impact_style(mitigation_2['impact'])}"
                        )

                        st.markdown(
                            f"**Mitigation Strategy:** "
                            f"{mitigation_2['strategy']}"
                        )

                        st.write(
                            mitigation_2["description"]
                        )

        st.divider()

        # ====================================================
        # LANGGRAPH WORKFLOW
        # ====================================================

        st.subheader(
            "🔄 LangGraph Agent Workflow"
        )

        st.caption(
            "Five reasoning stages from project data "
            "to the final strategic assessment."
        )

        workflow = run_langgraph_workflow(
            project_data=project,
            risk_score=result["risk_score"],
            feasibility_score=result["feasibility_score"],
        )

        for item in workflow:

            with st.container(border=True):

                left, middle, right = st.columns(
                    [0.08, 0.72, 0.20],
                    gap="small",
                )

                with left:

                    st.markdown(
                        f"## {item['step']}"
                    )

                with middle:

                    st.markdown(
                        f"### {item['icon']} {item['name']}"
                    )

                    st.write(
                        item["description"]
                    )

                with right:

                    st.success(
                        "✓ Completed"
                    )

        # ====================================================
        # STRATEGIC REASONING
        # ====================================================

        st.subheader("🧠 Strategic Reasoning")

        st.info(
            f"""
            The Prediction AI workflow converts **project data**
            into **risk analysis**, then transforms the analysis
            into **strategic recommendations** and
            **risk mitigation strategies**.

            **Current Risk Score:** {result['risk_score']:.1f}/100

            **Current Feasibility Score:** {result['feasibility_score']:.1f}%

            The recommendations are generated from the
            Milestone 2 assessment results so that the analysis
            leads to actionable next steps.
            """
        )


# ============================================================
# TAB 4 — DASHBOARD
# ============================================================

with tab4:

    st.header("Dashboard")

    st.caption(
        "Project, market, competitor and strategic overview."
    )

    project = st.session_state.get(
        "selected_project"
    )

    if project is None and projects:

        project = project_dict(
            projects[0]
        )

    if project:

        st.subheader("Project Overview")

        a, b, c = st.columns(3)

        with a:
            st.write("**Project Name**")
            st.write(project["project_name"])

        with b:
            st.write("**Target Market**")
            st.write(project["target_market"])

        with c:
            st.write("**Budget**")
            st.write(
                f"₹{float(project['budget']):,.2f}"
            )

        st.write("**Project Description**")
        st.write(project["project_description"])

        st.divider()

    else:

        st.info("No project available.")

    # ========================================================
    # MARKET
    # ========================================================

    st.subheader("Market Analysis")

    market = get_market_size()

    a, b, c = st.columns(3)

    a.metric(
        "TAM",
        market["tam"]["value"],
    )

    b.metric(
        "SAM",
        market["sam"]["value"],
    )

    c.metric(
        "SOM",
        market["som"]["value"],
    )

    trend = get_market_trends()

    chart_df = pd.DataFrame(
        {
            "Year": trend["years"],
            "Estimated Market Size ($B)": trend["values"],
        }
    )

    st.subheader("Market Trends")

    st.line_chart(
        chart_df,
        x="Year",
        y="Estimated Market Size ($B)",
    )

    st.divider()

    # ========================================================
    # COMPETITORS
    # ========================================================

    st.subheader("Competitor Landscape")

    competitors = get_competitors()

    if competitors:

        for competitor in competitors:

            st.write(
                f"**{competitor['name']}**"
            )

            a, b, c = st.columns(3)

            a.write(
                f"Market Share: "
                f"{competitor['market_share']}%"
            )

            b.write(
                f"Revenue: "
                f"{competitor['revenue']}"
            )

            c.write(
                f"Growth: "
                f"{competitor['growth']}"
            )

            st.progress(
                min(
                    max(
                        competitor["market_share"] / 100,
                        0,
                    ),
                    1,
                )
            )

    else:

        st.info(
            "No competitor information available."
        )

    # ========================================================
    # ASSESSMENT SUMMARY
    # ========================================================

    result = st.session_state.get(
        "milestone2_result"
    )

    if result:

        st.divider()

        st.subheader(
            "Assessment Summary"
        )

        a, b, c, d = st.columns(4)

        a.metric(
            "Risk Score",
            f"{result['risk_score']}/100",
        )

        b.metric(
            "Risk Status",
            result["risk_status"],
        )

        c.metric(
            "Success Probability",
            f"{result['success_probability']}%",
        )

        d.metric(
            "Feasibility",
            f"{result['feasibility_score']}%",
        )

        # ====================================================
        # MILESTONE 3 SUMMARY
        # ====================================================

        st.divider()

        st.subheader(
            "Milestone 3 Strategic Summary"
        )

        recommendations = generate_recommendations(
            risk_score=result["risk_score"],
            feasibility_score=result["feasibility_score"],
            project=project,
        )

        critical = sum(
            1
            for item in recommendations
            if item["priority"] == "Critical"
        )

        high = sum(
            1
            for item in recommendations
            if item["priority"] == "High"
        )

        medium = sum(
            1
            for item in recommendations
            if item["priority"] == "Medium"
        )

        a, b, c = st.columns(3)

        a.metric(
            "Critical Recommendations",
            critical,
        )

        b.metric(
            "High Priority",
            high,
        )

        c.metric(
            "Medium Priority",
            medium,
        )

        st.subheader(
            "Risk Mitigation Summary"
        )

        mitigations = generate_risk_mitigations(
            risk_score=result["risk_score"],
            feasibility_score=result["feasibility_score"],
        )

        a, b, c, d = st.columns(4)

        a.metric(
            "Market Risks",
            sum(
                item["category"] == "Market"
                for item in mitigations
            ),
        )

        b.metric(
            "Financial Risks",
            sum(
                item["category"] == "Financial"
                for item in mitigations
            ),
        )

        c.metric(
            "Technical Risks",
            sum(
                item["category"] == "Technical"
                for item in mitigations
            ),
        )

        d.metric(
            "Total Risks",
            len(mitigations),
        )

    else:

        st.info(
            "Complete the Risk Assessment to "
            "display the strategic summary."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Prediction AI • Milestone 3 • "
    "Recommendations • Risk Mitigation • Strategic Reasoning"
)