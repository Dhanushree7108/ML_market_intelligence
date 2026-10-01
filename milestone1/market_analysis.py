"""
Market analysis data used by the Dashboard.

These are fixed demo figures (as specified in the project brief) so the
Dashboard has something meaningful to render as soon as one project has
been submitted. A later milestone can swap get_market_size() /
get_competitors() for numbers derived from real analysis instead of
these static values — the dashboard route and template don't need to
change when that happens.
"""


def get_market_size():
    return {
        "tam": {"label": "TAM", "value": "$2.4B", "description": "Total Addressable Market"},
        "sam": {"label": "SAM", "value": "$850M", "description": "Serviceable Available Market"},
        "som": {"label": "SOM", "value": "$0.012M", "description": "Serviceable Obtainable Market"},
    }


def get_market_trends():
    years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
    values = [1.1, 1.35, 1.6, 1.9, 2.05, 2.25, 2.4]  # $B, illustrative growth curve
    return {"years": years, "values": values}


def get_competitors():
    return [
        {"name": "Competitor A", "market_share": 28, "revenue": "$45M", "revenue_millions": 45, "growth": "+12%"},
        {"name": "Competitor B", "market_share": 22, "revenue": "$38M", "revenue_millions": 38, "growth": "+8%"},
        {"name": "Competitor C", "market_share": 15, "revenue": "$25M", "revenue_millions": 25, "growth": "+5%"},
    ]


def get_market_funnel():
    """TAM -> SAM -> SOM as a proportional funnel (relative widths, 0-100)."""
    # $2.4B, $850M, $0.012M -> normalised to a readable funnel scale
    return [
        {"label": "TAM", "value": "$2.4B", "width": 100},
        {"label": "SAM", "value": "$850M", "width": 55},
        {"label": "SOM", "value": "$0.012M", "width": 15},
    ]


def get_dashboard_data():
    return {
        "market_size": get_market_size(),
        "market_trends": get_market_trends(),
        "competitors": get_competitors(),
        "market_funnel": get_market_funnel(),
    }
