"""Milestone 2 risk scoring engine."""


def calculate_risk(
    market_competition,
    team_expertise,
    resource_availability,
    innovation_level,
    market_research
):
    risk = 0

    # Market competition
    risk += {
        "High": 25,
        "Medium": 15,
        "Low": 5
    }.get(market_competition, 5)

    # Team expertise
    risk += {
        "Low": 20,
        "Medium": 10,
        "High": 5
    }.get(team_expertise, 5)

    # Resource availability
    risk += {
        "Limited": 20,
        "Moderate": 10,
        "Good": 5
    }.get(resource_availability, 5)

    # Innovation level
    risk += {
        "Low": 20,
        "Medium": 10,
        "High": 5
    }.get(innovation_level, 5)

    # Market research
    risk += {
        "Limited": 15,
        "Moderate": 8,
        "Strong": 3
    }.get(market_research, 3)

    return min(risk, 100)


def get_risk_status(score):
    if score >= 70:
        return "HIGH RISK"
    if score >= 40:
        return "MEDIUM RISK"
    return "LOW RISK"


def calculate_success_probability(risk_score):
    return max(0, 100 - risk_score)


def risk_breakdown(
    market_competition,
    team_expertise,
    resource_availability,
    innovation_level,
    market_research
):
    """
    Convert the five risk inputs into a simple 1-5
    risk breakdown for dashboard display.
    """

    return {
        "Market Risk": {
            "High": 5,
            "Medium": 3,
            "Low": 1
        }.get(market_competition, 1),

        "Technical Risk": {
            "Low": 5,
            "Medium": 3,
            "High": 1
        }.get(team_expertise, 1),

        "Operational Risk": {
            "Limited": 5,
            "Moderate": 3,
            "Good": 1
        }.get(resource_availability, 1),

        "Innovation Risk": {
            "Low": 5,
            "Medium": 3,
            "High": 1
        }.get(innovation_level, 1),

        "Research Risk": {
            "Limited": 5,
            "Moderate": 3,
            "Strong": 1
        }.get(market_research, 1),
    }