import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Local development: read .env from the project root.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def _setting(name, default=None):
    """Read a setting from environment first, then Streamlit Cloud Secrets."""
    value = os.getenv(name)
    if value is not None and value != "":
        return value

    try:
        import streamlit as st
        value = st.secrets.get(name)
        if value is not None and value != "":
            return str(value)
    except Exception:
        pass

    return default


def get_connection():
    """Connect to PostgreSQL using local .env or Streamlit Cloud Secrets."""
    return psycopg.connect(
        host=_setting("DB_HOST", "localhost"),
        dbname=_setting("DB_NAME", "ml_project"),
        user=_setting("DB_USER", "postgres"),
        password=_setting("DB_PASSWORD", ""),
        port=_setting("DB_PORT", "5432"),
    )


def fetch_projects():
    """Return all projects from the Milestone 1 projects table."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, project_name, project_description, target_market,
                       budget, competition, resources, objectives, created_at
                FROM projects
                ORDER BY id DESC
                """
            )
            return cursor.fetchall()
    finally:
        connection.close()


def insert_project(project_name, project_description, target_market, budget,
                   competition="", resources="", objectives=""):
    """Insert a project using the existing Milestone 1 schema."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO projects (
                    project_name, project_description, target_market, budget,
                    competition, resources, objectives
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (project_name, project_description, target_market, budget,
                 competition, resources, objectives),
            )
            new_id = cursor.fetchone()[0]
        connection.commit()
        return new_id
    finally:
        connection.close()
