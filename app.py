# ==========================================================
# AI CAREER ROADMAP GENERATOR
# PART 1A - FOUNDATION SETUP
# ==========================================================

# Import required libraries
import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
from ai.roadmap_generator import generate_career_roadmap
from ai.chat import career_chat
from database.database import create_connection, create_tables
from pdf.pdf_generator import create_roadmap_pdf, create_full_report_pdf
from database.analytics import log_visitor
# ==========================================================
# GEMINI AI CONFIGURATION
# ==========================================================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.set_option("client.showErrorDetails", False)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Career Roadmap Generator",
    page_icon="🚀",
    layout="wide"
)
    
st.markdown("""
<style>
:root{
    color-scheme: light !important;
}

html, body, [data-testid="stAppViewContainer"]{
    color-scheme: light !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_NAME = "career_roadmap.db"
create_tables()
if "visitor_logged" not in st.session_state:
    log_visitor("Guest", "visit")
    st.session_state.visitor_logged = True

# ==========================================================
# PASSWORD HASHING
# ==========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ==========================================================
# SESSION STATE VARIABLES
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""
    
if "ai_report" not in st.session_state:
    st.session_state.ai_report = ""
    
if "roadmap_generated" not in st.session_state:
    st.session_state.roadmap_generated = False

if "mentor_answer" not in st.session_state:
    st.session_state.mentor_answer = ""
    
if "preparation_questions" not in st.session_state:
    st.session_state.preparation_questions = ""

if "preparation_score" not in st.session_state:
    st.session_state.preparation_score = 0
    
if "user_qualification" not in st.session_state:
    st.session_state.user_qualification = ""

if "user_skills" not in st.session_state:
    st.session_state.user_skills = ""

if "selected_goal" not in st.session_state:
    st.session_state.selected_goal = ""


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    .main-title{
        text-align:center;
        font-size:42px;
        font-weight:bold;
        color:#1f2937;
        margin-top:10px;
    }

    .sub-title{
        text-align:center;
        font-size:18px;
        color:#4b5563;
        margin-bottom:20px;
    }
    
    /* Make input labels bold */
    label[data-testid="stWidgetLabel"] p {
        font-weight: bold !important;
    }

    .custom-box{
        background:white;
        padding:16px;
        border-radius:12px;
        border:1px solid #e5e7eb;
        box-shadow:0px 2px 8px rgba(0,0,0,0.08);
    }

    .welcome-box{
        background:#f0fdf4;
        padding:15px;
        border-radius:10px;
        border:1px solid #bbf7d0;
    }

    .success-box{
        background:#eff6ff;
        padding:15px;
        border-radius:10px;
        border:1px solid #bfdbfe;
    }
    
    .report-card{
        background: linear-gradient(135deg,#EFF6FF,#F8FAFC);
        border-left:6px solid #0EA5E9;
        border-radius:15px;
        padding:20px;
        margin-top:20px;
        margin-bottom:12px;
        box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    }
    
    .stContainer{
        background: linear-gradient(135deg,#F8FAFC,#EFF6FF);
        border:1px solid #BFDBFE;
        border-radius:16px;
        padding:22px;
        margin-top:15px;
        margin-bottom:15px;
        box-shadow:0px 4px 10px rgba(0,0,0,0.08);
    }

    .report-title{
        font-size:28px;
        font-weight:bold;
        color:#2563EB;
        margin-bottom:12px;
    }

    .report-content{
        font-size:16px;
        color:#374151;
        line-height:1.8;
    }

    div.stButton > button{
        width:100%;
        border-radius:10px;
        height:48px;
        font-weight:bold;
    }
    
    div[data-testid="stDownloadButton"] button{
        background-color:#0EA5E9 !important;
        color:white !important;
        border:none !important;
        border-radius:10px !important;
        height:48px !important;
        font-weight:bold !important;
    }

    div[data-testid="stDownloadButton"] button:hover{
        background-color:#0284C7 !important;
        color:white !important;
    }
    
    .download-btn button{
        background-color:#0EA5E9 !important;
        color:white !important;
        border:none !important;
        border-radius:10px !important;
        height:45px !important;
        font-weight:bold !important;
    }

    .download-btn button:hover{
        background-color:#0284C7 !important;
    }
    
    button[kind="primary"]{
    background-color:#0EA5E9 !important;
    color:white !important;
    border:none !important;
    }

    button[kind="primary"]:hover{
        background-color:#0284C7 !important;
        color:white !important;
    }
    
    /* Hide Streamlit Sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }

    /* Hide Sidebar Arrow Button */
    button[data-testid="collapsedControl"] {
        display: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# PROJECT HEADER
# ==========================================================

st.markdown(
    """
    <div class="main-title">
    🚀 AI Career Roadmap Generator
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-title">
    ✨ Build Your Career In Just Minutes
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        text-align:center;
        padding-left:20px;
        font-size:16px;
        color:#4B5563;
        margin-top:-8px;
        margin-bottom:20px;
    ">
    🌱🤖 An AI Career Guidance Solution ✨ by
    <span style="color:#2563EB;font-weight:bold;">
    Yashasri
    </span>
    🚀
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# PART 1B - LOGIN & REGISTER SYSTEM
# ==========================================================

# ----------------------------------------------------------
# REGISTER NEW USER
# ----------------------------------------------------------

def register_user(username, password):

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users(username, password, created_at)
            VALUES (?, ?, ?)
            """,
            (
                username,
                hash_password(password),
                datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            )
        )

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:

        conn.close()

        return False
def login_user(username, password):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user
    


# ----------------------------------------------------------
# LOGIN / REGISTER PAGE
# ----------------------------------------------------------

if not st.session_state.logged_in:

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )

    # ======================================================
    # LOGIN TAB
    # ======================================================

    with login_tab:

        st.markdown("### 🔐 Login To Your Account")

        login_username = st.text_input(
            "👤 Enter Username",
            key="login_username"
        )

        login_password = st.text_input(
            "🔑 Enter Password",
            type="password",
            key="login_password"
        )

        login_button = st.button(
            "🚀 Login"
        )

        if login_button:

            if (
                login_username.strip() == ""
                or
                login_password.strip() == ""
            ):

                st.warning(
                    "⚠️ Please enter username and password."
                )

            else:

                user = login_user(
                    login_username,
                    login_password
                )

                if user:

                    st.session_state.logged_in = True

                    st.session_state.username = (
                        login_username
                    )

                    st.success(
                        f"🎉 Welcome {login_username}"
                    )
                    log_visitor(login_username, "login")

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )

    # ======================================================
    # REGISTER TAB
    # ======================================================

    with register_tab:

        st.markdown(
            "### 📝 Create New Account"
        )

        register_username = st.text_input(
            "👤 Register Username",
            key="register_username"
        )

        register_password = st.text_input(
            "🔒 Create Password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "🔐 Confirm Password",
            type="password",
            key="confirm_password"
        )

        register_button = st.button(
            "✅ Register"
        )

        if register_button:

            if (
                register_username.strip() == ""
                or
                register_password.strip() == ""
                or
                confirm_password.strip() == ""
            ):

                st.warning(
                    "⚠️ Please fill all fields."
                )

            elif (
                register_password
                !=
                confirm_password
            ):

                st.error(
                    "❌ Passwords do not match."
                )
            elif not register_username.isalnum():

                st.error(
                    "❌ Username should contain only letters and numbers."
                )
            elif len(register_password) < 6:

                st.error(
                    "❌ Password must be at least 6 characters long."
                )

            else:

                result = register_user(
                    register_username,
                    register_password
                )

                if result:

                    st.success(
                        "🎉 Registration Successful!"
                    )

                    st.info(
                        "👉 Please login using your credentials."
                    )

                else:

                    st.error(
                        "❌ Username already exists."
                    )

# ==========================================================
# PART 2 - DASHBOARD + WELCOME + LOGOUT + CAREER FORM
# ==========================================================

if st.session_state.logged_in:

    st.markdown("---")

    col1, col2 = st.columns([8, 2])

    with col1:

        st.markdown(
            f"""
            <div class="welcome-box">
            <h3>🎉 Welcome {st.session_state.username}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        logout_button = st.button(
            "🚪 Logout"
        )

        if logout_button:

            st.session_state.logged_in = False
            st.session_state.username = ""

            st.rerun()
        history_button = st.button(
            "📜 My Roadmap History"
        )
        if history_button:
            st.switch_page("pages/roadmap_history.py")
        if st.session_state.username == "devi":
            admin_button = st.button("📊 Admin Dashboard")

            if admin_button:
                st.switch_page("pages/admin_dashboard.py")
    st.markdown("---")

    st.markdown(
        """
        ## 🚀 Career Roadmap Generator
        """
    )
    
    st.info(
        "✨ Fill the details below and generate your personalized career roadmap."
    )

    # ======================================================
    # NAME INPUT
    # ======================================================

    full_name = st.text_input(
        "👤 Enter Your Name",
        key="full_name"
    )

    if full_name:

        st.success(
            f"👋 Hi {full_name}, Nice To Meet You!"
        )

    # ======================================================
    # QUALIFICATION
    # ======================================================

    qualification = st.text_input(
        "🎓 Enter Your Qualification",
        key="qualification"
    )

    # ======================================================
    # SKILLS
    # ======================================================

    skills = st.text_area(
        "📚 Enter Your Skills (comma separated)",
        key="skills"
    )

    # ======================================================
    # CAREER GOALS
    # ======================================================

    career_options = [

        "AI Engineer",
        "Machine Learning Engineer",
        "Deep Learning Engineer",
        "Generative AI Engineer",
        "Prompt Engineer",
        "LLM Engineer",
        "NLP Engineer",
        "Computer Vision Engineer",

        "Data Scientist",
        "Data Analyst",
        "Business Analyst",

        "Python Developer",
        "Java Developer",
        "C++ Developer",

        "Software Engineer",
        "Software Developer",

        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",

        "React Developer",
        "Angular Developer",

        "Mobile App Developer",
        "Android Developer",
        "iOS Developer",

        "Cloud Engineer",
        "DevOps Engineer",

        "Cyber Security Analyst",
        "Ethical Hacker",

        "Blockchain Developer",

        "Game Developer",

        "UI UX Designer",

        "QA Engineer",
        "Automation Tester",

        "Product Manager",

        "Other"
    ]
    career_goal = st.selectbox(
        "🎯 Select Career Goal",
        career_options,
        key="career_goal"
    )

    custom_goal = ""

    if career_goal == "Other":

        custom_goal = st.text_input(
            "✍️ Enter Your Career Goal"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    # ======================================================
    # BUTTONS
    # ======================================================

    col1, col2 = st.columns([1, 0.2])

    with col1:
        generate_button = st.button(
            "🚀 Generate My Roadmap",
            type="primary",
            key="generate_btn"
        )

    with col2:
        clear_button = st.button(
            "🔄 Clear Roadmap",
            key="clear_btn"
        )
   
    # ======================================================
    # PART 3A - VALIDATION + ROADMAP GENERATION
    # ======================================================
    if clear_button:
        
        st.session_state.ai_report = ""
        st.session_state.roadmap_generated = False
        st.session_state.mentor_answer = ""
        st.session_state.preparation_questions = ""
        st.session_state.preparation_score = 0
        st.session_state.user_qualification = ""
        st.session_state.user_skills = ""
        st.session_state.selected_goal = ""

        st.rerun()
    if generate_button:
        selected_goal = custom_goal.strip() if career_goal == "Other" else career_goal
        
        if full_name.strip() == "" or selected_goal.strip() == "":
            st.warning("⚠️ Please Enter Your Name And Select A Career Goal")
        else:
            st.balloons()

            try:
                with st.spinner("🤖 AI is generating your personalized career roadmap..."):
                    st.session_state.ai_report = generate_career_roadmap(
                        full_name=full_name,
                        qualification=qualification,
                        skills=skills,
                        career_goal=selected_goal
                    )

            except Exception as e:

                error = str(e).lower()

                if (
                    "429" in error
                    or "quota" in error
                    or "resource exhausted" in error
                ):
                    st.error(
                        "⚠️ AI service is temporarily unavailable because the daily usage limit has been reached. Please try again later."
                    )

                elif (
                    "connection" in error
                    or "network" in error
                    or "internet" in error
                    or "timeout" in error
                ):
                    st.error(
                        "🌐 Internet connection is unavailable or unstable. Please check your connection and try again."
                    )

                else:
                    st.error(
                        "❌ Something went wrong while generating your roadmap. Please try again in a few minutes."
                    )

                st.stop()
            conn = create_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO history(
                    username,
                    full_name,
                    qualification,
                    skills,
                    career_goal,
                    generated_date,
                    ai_report,
                    prep_questions,
                    prep_answers,
                    prep_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    st.session_state.username,
                    full_name,
                    qualification,
                    skills,
                    selected_goal,
                    datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    st.session_state.ai_report,
                    "",
                    "",
                    ""
                )
            )

            conn.commit()
            conn.close()
            st.success("✅ Roadmap Generated Successfully!")

            st.session_state.roadmap_generated = True
            st.session_state.selected_goal = selected_goal
            st.session_state.preparation_questions = ""
            st.session_state.user_qualification = qualification
            st.session_state.user_skills = skills
    # ==========================================================
    # DISPLAY AI REPORT (Persistent if generated)
    # ==========================================================

    if st.session_state.get("roadmap_generated"):
        st.markdown("---")
        st.markdown("## 🎯 Your Personalized Career Report")
        
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

        clean_response = st.session_state.ai_report
        clean_response = re.sub(r"<[^>]*>", "", clean_response)
        clean_response = re.sub(r"#+\s*", "", clean_response)
        clean_response = re.sub(r"\n\s*\n\s*\n+", "\n\n", clean_response)
        
        for i, header in enumerate(section_headers):
            start = clean_response.find(header)
            if start == -1: continue
            
            start_content = start + len(header)
            end = clean_response.find(section_headers[i+1], start_content) if i + 1 < len(section_headers) else len(clean_response)
            content = clean_response[start_content:end]
            content = re.sub(r"\n\s*[🎯📊🌱🗺️💼📚🤖💰✅💬🌟]\s*", "\n", content)
            content = content.strip()
            content = re.sub(r"\s*•\s*", "\n- ", content)
            content = re.sub(r"(What to Learn:|What to Practice:|Goal to Complete:|Career Opportunities|What to Learn Next|AI Tools|Salary Growth|Career Preparation Check)", r"\n\1", content)
            
            content = content.strip()
            content = re.sub(r"\n{2,}", "\n", content)
            content = re.sub(
                r"(Phase \d+:.*)",
                r"<h3 style='color:#2563EB; font-weight:bold; margin:0px;'>\1</h3>",
                content
            )

            content = re.sub(
                r"</h3>\s*\n+",
                "</h3>",
                content
            )

            content = re.sub(
                r"(What to Learn:|What to Practice:|Goal to Complete:|Short Explanation:)",
                r"<b style='color:#1E3A8A;'>\1</b>",
                content
            )
            
            content = content.replace("**", "")
            if header == "🗺️ Career Roadmap":
                content = re.sub(r"\n\s*\n", "\n", content)
            formatted_content = content.replace("\n", "<br>")
            if header == "✅ Career Preparation Check":

                questions = []

                for line in content.split("\n"):
                    line = line.strip()

                    if not line:
                        continue

                    if "Career Preparation Check" in line:
                        continue

                    questions.append(line)

                st.markdown("### ✅ Career Preparation Check")
                st.write("Answer the following questions to check your career preparation.")

                answers = []

                for q_no, question in enumerate(questions):
                    st.markdown(
                        f"""
                        <p style="margin-bottom:5px; font-weight:600;">
                        {question}
                        </p>
                        """,
                        unsafe_allow_html=True
                    )

                    answer = st.radio(
                        "",
                        ["Yes", "No"],
                        key=f"prep_{q_no}",
                        horizontal=True
                    )

                    answers.append(answer)

                    st.markdown(
                        "<hr style='margin-top:5px; margin-bottom:8px;'>",
                        unsafe_allow_html=True
                    )

                if st.button(
                    "📊 Calculate Preparation Score",
                    key="prep_score",
                    type="primary"
                ):

                    yes_count = answers.count("Yes")

                    score = int(
                        (yes_count / len(questions)) * 100
                    )
                    conn = create_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        UPDATE history
                        SET
                            prep_questions=?,
                            prep_answers=?,
                            prep_score=?
                        WHERE id = (
                            SELECT MAX(id)
                            FROM history
                            WHERE username=?
                        )
                        """,
                        (
                            "\n".join(questions),
                            "\n".join(answers),
                            str(score),
                            st.session_state.username
                        )
                    )

                    conn.commit()
                    conn.close()

                    st.progress(score / 100)

                    st.markdown(
                        """
                        <h2 style='margin-bottom:0px; margin-top:8px; color:#2563EB;'>
                            📊 Preparation Score
                        </h2>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown("<div style='margin-top:-18px;'></div>", unsafe_allow_html=True)

                    st.markdown(
                        f"""
                        <h1 style="
                            margin-top:-35px;
                            margin-bottom:0px;
                            font-size:42px;
                            font-weight:bold;
                            color:#111827;
                        ">
                            {score}%
                        </h1>
                        """,
                        unsafe_allow_html=True
                    )

                    if score >= 80:

                        st.success(
                            "🚀 Excellent! You are well prepared for your career goal."
                        )

                    elif score >= 50:

                        st.info(
                            "🌱 Good progress! Keep improving your skills to become career ready."
                        )

                    else:

                        st.warning(
                            "📚 Keep learning consistently. Every small step brings you closer to your dream career."
                        )
                continue 
            colors = ["#EFF6FF", "#F0FDF4", "#FEFCE8", "#FFF7ED", "#FDF2F8", "#F5F3FF", "#ECFEFF", "#F9FAFB", "#EEF2FF", "#F0FDFA", "#FEF2F2"]
            
            st.markdown(f"""
                <div style="background:{colors[i]}; border-left:7px solid #2563EB; border-radius:18px; padding:22px; margin-bottom:20px; box-shadow:0 3px 12px rgba(0,0,0,.08);">
                    <h3 style="color:#1E3A8A;">{header}</h3>
                    <div style="font-size:16px; line-height:1.45; color:#374151;">{formatted_content}</div>
                </div>
            """, unsafe_allow_html=True)
            if header == "🗺️ Career Roadmap":
                pdf_content = re.sub(r"<[^>]*>", "", content)
                pdf_content = pdf_content.replace("What to Learn:", "\nWhat to Learn:")
                pdf_content = pdf_content.replace("What to Practice:", "\nWhat to Practice:")
                pdf_content = pdf_content.replace("Goal to Complete:", "\nGoal to Complete:")
                pdf_content = pdf_content.replace("Short Explanation:", "\nShort Explanation:")

                pdf_file = "AI_Career_Roadmap.pdf"

                create_roadmap_pdf(
                    pdf_content,
                    pdf_file
                )

                with open(pdf_file, "rb") as file:
                    st.markdown('<div class="download-btn">', unsafe_allow_html=True)
                    st.download_button(
                        label="📄 Download Career Roadmap PDF",
                        data=file,
                        file_name="AI_Career_Roadmap.pdf",
                        mime="application/pdf",
                        key="roadmap_pdf_download"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
        
        # ==========================================================
        # AI CAREER CHATBOX
        # ==========================================================
        st.markdown("---")  
        st.markdown("## 💬 AI Career Chatbox")  
        
        chat_question = st.text_input("Ask your career question", key="chat_input")  
        
        if st.button("🤖 Ask AI Mentor", key="mentor_btn"):  
            if chat_question.strip():  
                try:

                    with st.spinner("AI Mentor is thinking..."):

                        st.session_state.mentor_answer = career_chat(
                            user_question=chat_question,
                            career_goal=st.session_state.selected_goal,
                            qualification=st.session_state.user_qualification,
                            skills=st.session_state.user_skills
                        )

                except Exception as e:

                    error = str(e).lower()

                    if (
                        "429" in error
                        or "quota" in error
                        or "resource exhausted" in error
                    ):
                        st.error(
                            "⚠️ AI service is temporarily unavailable because the daily usage limit has been reached. Please try again later."
                        )

                    elif (
                        "connection" in error
                        or "network" in error
                        or "internet" in error
                        or "timeout" in error
                    ):
                        st.error(
                            "🌐 Internet connection is unavailable or unstable. Please check your connection and try again."
                        )

                    else:
                        st.error(
                            "❌ Unable to get a response from the AI Mentor. Please try again later."
                        )
            else:  
                st.warning("Please enter your question.")  

        if "mentor_answer" in st.session_state and st.session_state.mentor_answer:  
            st.success("AI Mentor Response")  
            st.write(st.session_state.mentor_answer)
        # ==========================================================
        # THANK YOU SECTION
        # ==========================================================

        st.markdown("---")

        st.markdown(
            """
            <div style="
                max-width:800px;
                width:95%;
                margin:40px auto;
                padding:35px;
                background:#F8FAFC;
                border:1px solid #BFDBFE;
                border-radius:20px;
                text-align:center;
            ">

            <h2 style="
                color:#2563EB;
                font-size:34px;
                font-weight:bold;
            ">
            💙✨ Thank You!
            </h2>

            <p>
            Wishing you success in your career journey.<br>
            May your future be filled with learning, growth, and great opportunities.
            </p>

            <p>
            📚 Keep Learning • 🌱 Keep Growing • 🚀 Keep Building
            </p>

            <p style="
            color:#2563EB;
            font-weight:bold;
            ">
            💙 Designed & Developed with ❤️ by Yashasri💫
            </p>

            <p>
            © 2026 AI Career Roadmap Generator
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )