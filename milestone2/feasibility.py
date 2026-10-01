"""Milestone 2 feasibility calculation."""


def calculate_feasibility(
    market_opportunity,
    team_capability,
    competitive_advantage,
    resource_availability
):
    """
    Calculate overall feasibility score as the average
    of the four feasibility factors.
    """

    scores = [
        market_opportunity,
        team_capability,
        competitive_advantage,
        resource_availability
    ]

    return round(sum(scores) / len(scores))


def feasibility_label(score):
    """
    Return a simple feasibility label based on the score.
    """

    if score >= 70:
        return "HIGH FEASIBILITY"
    elif score >= 40:
        return "MEDIUM FEASIBILITY"
    else:
        return "LOW FEASIBILITY"