"""Dashboard demo market-analysis data used only by Milestone 2."""


def get_market_size():
    return {
        "tam": {"label": "TAM", "value": "$2.4B", "description": "Total Addressable Market"},
        "sam": {"label": "SAM", "value": "$0.85B", "description": "Serviceable Available Market"},
        "som": {"label": "SOM", "value": "$0.012M", "description": "Serviceable Obtainable Market"},
    }


def get_market_trends():
    return {
        "years": [2020, 2021, 2022, 2023, 2024, 2025, 2026],
        "values": [1.1, 1.35, 1.6, 1.9, 2.05, 2.25, 2.4],
    }


def get_competitors():
    return [
        {"name": "Competitor A", "market_share": 28, "revenue": "$45M", "growth": "+12%"},
        {"name": "Competitor B", "market_share": 22, "revenue": "$38M", "growth": "+8%"},
        {"name": "Competitor C", "market_share": 15, "revenue": "$25M", "growth": "+5%"},
    ]
