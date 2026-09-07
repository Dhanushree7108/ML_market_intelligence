"""Milestone 2 risk scoring engine."""


def calculate_risk(market_competition, team_expertise, resource_availability, innovation_level, market_research):
    risk = 0

    risk += {"High": 25, "Medium": 15, "Low": 5}.get(market_competition, 5)
    risk += {"Low": 20, "Medium": 10, "High": 5}.get(team_expertise, 5)
    risk += {"Limited": 20, "Moderate": 10, "Good": 5}.get(resource_availability, 5)
    risk += {"Low": 20, "Medium": 10, "High": 5}.get(innovation_level, 5)
    risk += {"Limited": 15, "Moderate": 8, "Strong": 3}.get(market_research, 3)

    return min(risk, 100)


def get_risk_status(score):
    if score >= 70:
        return "HIGH RISK"
    if score >= 40:
        return "MEDIUM RISK"
    return "LOW RISK"


def calculate_success_probability(risk_score):
    return max(0, 100 - risk_score)
