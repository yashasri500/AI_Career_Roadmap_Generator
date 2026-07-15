import streamlit as st
from database.database import create_connection
from pdf.pdf_generator import create_full_report_pdf
import re


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="My Roadmap History",
    page_icon="📜",
    layout="wide"
)
st.markdown(
    """
    <style>

    section[data-testid="stSidebar"] {
        display: none;
    }

    button[data-testid="collapsedControl"] {
        display: none;
    }
    
    div.stButton > button {
        white-space: nowrap;
        width: 180px;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="text-align:center;">
    <h1 style="color:#1f2937;">
    🚀 AI Career Roadmap Generator
    </h1>
    <p style="font-size:18px;color:#4b5563;">
    ✨ Build Your Career In Just Minutes
    </p>
    <p style="
    text-align:center;
    padding-left:20px;
    font-size:16px;
    color:#4B5563;
    margin-top:8px;
    ">
    🌱🤖 An AI Career Guidance Solution ✨ by
    <span style="color:#2563EB;font-weight:bold;">
    Yashasri
    </span>
    🚀
    </p>
    </div>
    """,
    unsafe_allow_html=True
)
# ==========================================================
# HISTORY SECTION
# ==========================================================
st.markdown(
    """
    <hr style="
    border:0;
    height:1px;
    background:#D1D5DB;
    margin:25px 0;
    ">
    """,
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns([1,8,1])

with col1:
    if st.button("⬅️ Back To Dashboard"):
        st.switch_page("app.py")

with col2:
    st.markdown(
        """
        <h2 style="
            text-align:center;
            color:#2563EB;
        ">
        📜 My Roadmap History
        </h2>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# CHECK LOGIN USER
# ==========================================================

if "username" not in st.session_state:

    st.warning("Please login first.")
    st.stop()
# ==========================================================
# ROADMAP VIEW STATE
# ==========================================================

if "show_roadmap" not in st.session_state:
    st.session_state.show_roadmap = None


# ==========================================================
# FETCH HISTORY
# ==========================================================

conn = create_connection()

cursor = conn.cursor()

cursor.execute(
    """
    SELECT 
    id,
    career_goal,
    generated_date,
    ai_report,
    full_name,
    qualification,
    skills,
    prep_questions,
    prep_answers,
    prep_score
    FROM history
    WHERE username=?
    ORDER BY id DESC
    """,
    (st.session_state.username,)
)

history_data = cursor.fetchall()

conn.close()


# ==========================================================
# DISPLAY HISTORY
# ==========================================================

if history_data:

    for item in history_data:

        st.markdown(
            f"""
            <div style="
                background:#EFF6FF;
                padding:22px;
                border-radius:18px;
                border:1px solid #BFDBFE;
                margin:20px auto;
                max-width:800px;
                box-shadow:0 3px 10px rgba(0,0,0,0.08);
            ">

            <h3 style="color:#1E40AF;">
            🎯 {item[1]}
            </h3>

            <p style="
            font-size:16px;
            color:#374151;
            ">
            📅 Generated Date & Time: {item[2]}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ==================================================
        # BUTTON SECTION
        # ==================================================

        col_space1, col1, col2, col3, col_space2 = st.columns(
            [2, 1, 1, 1, 2]
        )

        with col1:

            if st.session_state.show_roadmap == item[0]:

                view = st.button(
                    "🙈 Hide Roadmap",
                    key=f"hide_{item[0]}"
                )

            else:

                view = st.button(
                    "👁️ View Roadmap",
                    key=f"view_{item[0]}"
                )


        with col2:

            delete = st.button(
                "🗑️ Delete History",
                key=f"delete_{item[0]}"
            )


        with col3:

            download = st.button(
                "⬇️ Download Full Report",
                key=f"download_btn_{item[0]}"
            )

        # ==================================================
        # DELETE HISTORY
        # ==================================================

        if delete:

            conn = create_connection()

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM history WHERE id=?",
                (item[0],)
            )

            conn.commit()

            conn.close()

            st.success(
                "✅ History deleted successfully."
            )

            st.rerun()
        if download:

            pdf_file = f"AI_Full_Career_Report_{item[0]}.pdf"

            create_full_report_pdf(
                name=item[4],
                qualification=item[5],
                skills=item[6],
                career_goal=item[1],
                report=item[3],
                prep_questions=item[7],
                prep_answers=item[8],
                prep_score=item[9],
                filename=pdf_file
            )

            with open(pdf_file, "rb") as file:

                st.download_button(
                    label="⬇️ Download Full Report",
                    data=file,
                    file_name=pdf_file,
                    mime="application/pdf",
                    key=f"full_report_download_{item[0]}"
                )

        # ==================================================
        # VIEW ROADMAP
        # ==================================================

        if view:

            if st.session_state.show_roadmap == item[0]:
                st.session_state.show_roadmap = None
                st.rerun()

            else:
                st.session_state.show_roadmap = item[0]
                st.rerun()


        if st.session_state.show_roadmap == item[0]:

            st.markdown("---")

            st.markdown(
                "## 🗺️ Career Roadmap"
            )

            clean_response = item[3]

            section_headers = [
                "🎯 Career Summary",
                "📊 Career Readiness",
                "🌱 Current Stage",
                "🗺️ Career Roadmap",
                "💼 Career Opportunities",
                "📚 What to Learn Next",
                "🤖 AI Tools",
                "💰 Salary Growth",
                "✅ Career Preparation Check",
                "🌟 Motivation"
            ]

            import re

            clean_response = re.sub(
                r"<[^>]*>",
                "",
                clean_response
            )

            clean_response = re.sub(
                r"#+\s*",
                "",
                clean_response
            )

            clean_response = re.sub(
                r"\n\s*\n\s*\n+",
                "\n\n",
                clean_response
            )


            colors = [
                "#EFF6FF",
                "#F0FDF4",
                "#FEFCE8",
                "#FFF7ED",
                "#FDF2F8",
                "#F5F3FF",
                "#ECFEFF",
                "#F9FAFB",
                "#EEF2FF",
                "#F0FDFA"
            ]


            for i, header in enumerate(section_headers):

                start = clean_response.find(header)

                if start == -1:
                    continue


                start_content = start + len(header)


                end = (
                    clean_response.find(
                        section_headers[i+1],
                        start_content
                    )
                    if i + 1 < len(section_headers)
                    else len(clean_response)
                )


                content = clean_response[
                    start_content:end
                ].strip()
                content = re.sub(r"\n{2,}", "\n", content)
                content = content.strip()
                content = re.sub(
                    r"(Phase\s+\d+:.*)",
                    r"<h3 style='color:#2563EB;font-weight:bold;margin:12px 0 8px 0;'>\1</h3>",
                    content
                )

                formatted = content.replace("\n", "<br>")

                st.markdown(
                    f"""
                    <div style="
                        background:{colors[i]};
                        border-left:6px solid #2563EB;
                        border-radius:18px;
                        padding:20px;
                        margin-bottom:18px;
                        box-shadow:0 3px 10px rgba(0,0,0,.08);
                    ">

                    <h3 style="
                    color:#1E3A8A;
                    ">
                    {header}
                    </h3>

                    <div style="
                    font-size:16px;
                    line-height:1.7;
                    ">
                    {formatted}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )
else:

    st.info(
        "No roadmap history found."
    )