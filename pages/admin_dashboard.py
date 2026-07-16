import streamlit as st
from database.database import create_connection

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Admin Analytics Dashboard")

conn = create_connection()
cursor = conn.cursor()

# Total Users
cursor.execute("SELECT COUNT(*) FROM users")
total_users = cursor.fetchone()[0]

# Total Visitors
cursor.execute("SELECT COUNT(*) FROM analytics WHERE event='visit'")
total_visitors = cursor.fetchone()[0]

# Total Logins
cursor.execute("SELECT COUNT(*) FROM analytics WHERE event='login'")
total_logins = cursor.fetchone()[0]

# Total Roadmaps
cursor.execute("SELECT COUNT(*) FROM history")
total_roadmaps = cursor.fetchone()[0]

conn.close()

col1, col2 = st.columns(2)

with col1:
    st.metric("👥 Registered Users", total_users)
    st.metric("👀 Total Visitors", total_visitors)

with col2:
    st.metric("🔑 Total Logins", total_logins)
    st.metric("🗺️ Roadmaps Generated", total_roadmaps)
st.markdown("---")
st.subheader("👥 Registered Users Details")

conn = create_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT username, created_at
FROM users
ORDER BY id DESC
""")

users = cursor.fetchall()

conn.close()

if users:
    for username, created_at in users:
        st.write(f"👤 **Username:** {username}")
        st.write(f"📅 **Registered On:** {created_at}")
        st.markdown("---")
else:
    st.info("No registered users found.")

if st.button("⬅️ Back"):
    st.switch_page("app.py")