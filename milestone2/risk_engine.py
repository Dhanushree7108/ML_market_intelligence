"""Milestone 2 risk scoring engine.

The scoring follows the Milestone 2 plan supplied for the project:
competition 25/15/5, team 20/10/5, resources 20/10/5,
innovation 20/10/5 and market research 15/8/3.
"""

RISK_POINTS = {
    "market_competition": {"High": 25, "Medium": 15, "Low": 5},
    "team_expertise": {"Low": 20, "Medium": 10, "High": 5},
    "resource_availability": {"Limited": 20, "Moderate": 10, "Good": 5},
    "innovation_level": {"Low": 20, "Medium": 10, "High": 5},
    "market_research": {"Limited": 15, "Moderate": 8, "Strong": 3},
}


def calculate_risk(market_competition, team_expertise, resource_availability,
                   innovation_level, market_research):
    score = (
        RISK_POINTS["market_competition"].get(market_competition, 5)
        + RISK_POINTS["team_expertise"].get(team_expertise, 5)
        + RISK_POINTS["resource_availability"].get(resource_availability, 5)
        + RISK_POINTS["innovation_level"].get(innovation_level, 5)
        + RISK_POINTS["market_research"].get(market_research, 3)
    )
    return min(score, 100)


def get_risk_status(score):
    if score >= 70:
        return "HIGH RISK"
    if score >= 40:
        return "MEDIUM RISK"
    return "LOW RISK"


def calculate_success_probability(risk_score):
    return max(0, 100 - risk_score)


def risk_breakdown(market_competition, team_expertise, resource_availability,
                   innovation_level, market_research):
    """Return a five-category 1-5 display matching the dashboard style."""
    values = {
        "Market Risk": RISK_POINTS["market_competition"].get(market_competition, 5),
        "Financial Risk": RISK_POINTS["resource_availability"].get(resource_availability, 5),
        "Competition": RISK_POINTS["market_competition"].get(market_competition, 5),
        "Technical": RISK_POINTS["team_expertise"].get(team_expertise, 5),
        "Operational": RISK_POINTS["innovation_level"].get(innovation_level, 5),
    }
    # Convert the 5-25/20-point components to a simple 1-5 risk display.
    max_points = {
        "Market Risk": 25, "Financial Risk": 20, "Competition": 25,
        "Technical": 20, "Operational": 20,
    }
    return {k: round(1 + 4 * (v / max_points[k]), 1) for k, v in values.items()}
