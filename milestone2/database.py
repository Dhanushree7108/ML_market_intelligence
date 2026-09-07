import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Load the shared .env from the project root so both milestones use the same DB.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "ml_project"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        port=os.getenv("DB_PORT", "5432"),
    )
