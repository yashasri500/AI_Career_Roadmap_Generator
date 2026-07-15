import sqlite3

DATABASE_NAME = "career_roadmap.db"


def create_connection():
    """
    Create and return SQLite database connection.
    """

    connection = sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )

    return connection


def create_tables():
    """
    Create all required database tables.
    """

    connection = create_connection()
    cursor = connection.cursor()

    # ==========================
    # Users Table
    # ==========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT
        )
    """)

    # ==========================
    # Roadmaps History Table
    # ==========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            full_name TEXT,
            qualification TEXT,
            skills TEXT,
            career_goal TEXT,
            generated_date TEXT,
            ai_report TEXT,
            prep_questions TEXT,
            prep_answers TEXT,
            prep_score TEXT
        )
    """)

    connection.commit()
    connection.close()