import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Milestone 2 reads the same PostgreSQL database created by Milestone 1.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "ml_project"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        port=os.getenv("DB_PORT", "5432"),
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
            rows = cursor.fetchall()
        return rows
    finally:
        connection.close()


def insert_project(project_name, project_description, target_market, budget,
                    competition="", resources="", objectives=""):
    """Optional Milestone 2 project-input helper; uses the existing M1 schema."""
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
                (
                    project_name, project_description, target_market, budget,
                    competition, resources, objectives,
                ),
            )
            new_id = cursor.fetchone()[0]
        connection.commit()
        return new_id
    finally:
        connection.close()
