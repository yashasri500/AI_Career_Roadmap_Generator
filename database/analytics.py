from database.database import create_connection
from datetime import datetime


def log_visitor(username="Guest", event="visit"):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analytics(username, event, event_time)
        VALUES (?, ?, ?)
    """, (
        username,
        event,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ))

    conn.commit()
    conn.close()