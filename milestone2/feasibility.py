"""Milestone 2 feasibility scoring engine."""


def calculate_feasibility(market_opportunity, team_capability,
                          competitive_advantage, resource_availability):
    score = (
        market_opportunity
        + team_capability
        + competitive_advantage
        + resource_availability
    ) / 4
    return round(score)


def feasibility_label(score):
    if score >= 70:
        return "Highly Feasible"
    if score >= 50:
        return "Feasible"
    return "Needs Improvement"
