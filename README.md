# 🚀 AI Career Roadmap Generator

## ✨ Build Your Career In Just Minutes

An AI-powered career guidance application that helps students and professionals create personalized career roadmaps based on their qualification, current skills, and career goals.

This application uses Generative AI to analyze user information and generate structured career guidance including learning paths, skill improvement suggestions, career opportunities, preparation checks, AI mentor support, and downloadable career reports.

Developed by **Yashasri** 🚀

---

# 📌 Project Overview

Choosing the right career path is challenging for many students and beginners.

The **AI Career Roadmap Generator** provides personalized career guidance using Artificial Intelligence. It helps users understand their current level, identify required skills, and follow a structured learning roadmap for their desired career.

Users can provide:

- Name
- Qualification
- Current Skills
- Career Goal

Based on these details, the application generates a personalized career report according to the user's background and selected career path.

---

# 🎯 Problem Statement

Many students and beginners are confused about:

- Which career path to choose
- What skills they need to learn
- How to prepare for industry roles
- What tools and technologies are required
- How to improve their career readiness

This project solves these problems by providing AI-based personalized career guidance.

---

# 🌟 Key Features

## 🔐 User Authentication System

The application provides a secure user management system.

Features:

- User registration
- User login
- Password hashing using SHA256
- Unique user accounts
- Session-based authentication
- Secure user data storage using SQLite database

---

## 🤖 AI Career Roadmap Generation

The core feature of the application is AI-powered career roadmap generation.

Google Gemini AI analyzes:

- User qualification
- Current skills
- Selected career goal

and generates a personalized career report.

Generated report includes:

- 🎯 Career Summary
- 📊 Career Readiness
- 🌱 Current Stage Analysis
- 🗺️ 5 Phase Career Roadmap
- 💼 Career Opportunities
- 📚 Skills To Learn Next
- 🤖 AI Tools Recommendation
- 💰 Salary Growth Information
- ✅ Career Preparation Check
- 🌟 Motivation Section

---

## 🗺️ Personalized Career Roadmap

The AI creates a structured learning roadmap based on the selected career.

Each roadmap contains:

### Phase Based Learning Plan

Every phase includes:

- What to Learn
- What to Practice
- Goal to Complete
- Short Explanation

The roadmap dynamically changes depending on:

- Qualification level
- Existing skills
- Career goal

---

## 💬 AI Career Chatbox

The application includes an AI Career Mentor chatbot.

Users can ask career-related questions and get guidance.

Features:

- Career doubt clarification
- Skill improvement suggestions
- Learning advice
- Practical career recommendations
- Simple explanations

---

## 📊 Career Preparation Check

The application evaluates user preparation level.

Features:

- Generates 10 personalized Yes/No questions
- Questions depend on user's career goal
- Calculates preparation percentage
- Shows progress visualization
- Provides readiness feedback

---

## 📜 Roadmap History Management

Users can access their previously generated career reports.

Features:

- Automatically saves generated roadmaps
- View previous reports
- Open roadmap history page
- Delete unwanted history
- Download complete career reports

---

## 📄 PDF Report Generation

The application generates downloadable PDF documents.

Available reports:

- Career Roadmap PDF
- Full Career Report PDF

PDF generation is implemented using ReportLab.

---

# 🛠️ Technology Stack

## Programming Language

- Python

## Frontend Framework

- Streamlit

## Artificial Intelligence

- Google Gemini Generative AI

## Database

- SQLite Database

## PDF Generation

- ReportLab

## Environment Configuration

- Python-dotenv

## Version Control

- Git
- GitHub

---

# 📂 Project Structure

```text
AI_CAREER_ROADMAP_GENERATOR

│
├── .streamlit
│   └── config.toml
│
├── ai
│   ├── chat.py
│   ├── prompts.py
│   └── roadmap_generator.py
│
├── database
│   ├── database.py
│   └── models.py
│
├── pages
│   └── roadmap_history.py
│
├── pdf
│   └── pdf_generator.py
│
├── app.py
├── career_roadmap.db
├── requirements.txt
├── .env
├── .gitignore
└── README.md

# ⚙️ Installation and Setup

Follow these steps to run the AI Career Roadmap Generator application on your local system.

## 1. Clone the Repository

Download or clone the project repository from GitHub and open the project folder.

## 2. Create Virtual Environment

Create a Python virtual environment to keep project dependencies separate from the system environment.

For Windows:

    python -m venv venv

Activate the environment:

    venv\Scripts\activate

For Mac/Linux:

    python -m venv venv

    source venv/bin/activate

---

# 📦 Install Required Packages

Install all required Python libraries using the requirements file.

    pip install -r requirements.txt

The project uses the following major packages:

- Streamlit
- Google Generative AI
- SQLite
- ReportLab
- Python-dotenv
- Pandas
- NumPy

---

# 🔑 Environment Configuration

This project uses Google Gemini Generative AI for generating personalized career roadmaps.

Create a file named:

.env

inside the project root directory.

Add your Gemini API key:

GEMINI_API_KEY=your_api_key_here

Important:

- Keep your API key private.
- Do not upload the .env file to GitHub.
- The .gitignore file prevents sensitive files from being committed.

---

# ▶️ Running the Application

Start the Streamlit application using:

    streamlit run app.py

After running successfully, the application opens in the browser.

---

# 🖥️ Application Workflow

## 1. User Registration

Users can create a personal account.

Registration includes:

- Username creation
- Password creation
- Secure password hashing

---

## 2. User Login

Registered users can securely login into their account.

After login, users can access their personalized career dashboard.

---

## 3. Career Information Input

Users provide their details:

- Name
- Qualification
- Current Skills
- Career Goal

---

## 4. AI Career Roadmap Generation

Google Gemini AI analyzes user information and generates a personalized career report.

The AI report contains:

- Career Summary
- Career Readiness Percentage
- Current Learning Stage
- 5 Phase Career Roadmap
- Career Opportunities
- Skills To Learn Next
- AI Tools Recommendation
- Salary Growth Information
- Career Preparation Check
- Motivation

---

## 5. AI Career Mentor Chatbox

Users can ask career-related questions and get guidance from an AI Career Mentor.

The chatbot provides:

- Career advice
- Learning suggestions
- Skill improvement guidance
- Practical recommendations

---

## 6. Roadmap History Management

The application stores previously generated career reports.

Users can:

- View previous roadmaps
- Open saved reports
- Delete history
- Download full career reports

---

# 🗄️ Database Design

The project uses SQLite database for storing user information and generated roadmap history.

## Users Table

Stores:

- User ID
- Username
- Password Hash
- Account Creation Date

---

## History Table

Stores:

- Username
- Full Name
- Qualification
- Skills
- Career Goal
- Generated Date
- AI Generated Report
- Preparation Questions
- User Answers
- Preparation Score

---

# 🧩 Module Description

## app.py

Main application file.

Responsibilities:

- Streamlit user interface
- Registration and login system
- Dashboard management
- Career form handling
- AI report display
- PDF download functionality

---

## ai/roadmap_generator.py

Responsible for:

- Google Gemini AI integration
- Generating personalized career roadmaps
- Processing AI responses

---

## ai/prompts.py

Contains:

- AI prompt templates
- Career report generation instructions
- Structured output format rules

---

## ai/chat.py

Handles:

- AI Career Mentor chatbot
- Career question answering
- Personalized career suggestions

---

## database/database.py

Responsible for:

- SQLite database connection
- Creating database tables
- Managing database operations

---

## database/models.py

Contains:

- User data model
- Career profile model
- Roadmap history model

---

## pdf/pdf_generator.py

Handles:

- Career roadmap PDF generation
- Full career report PDF generation

---

## pages/roadmap_history.py

Provides:

- Saved roadmap history page
- Previous report viewing
- Report download options

---

# 🚀 Deployment

The application is deployed as a Streamlit web application.

Deployment provides:

- Online accessibility
- Shareable application URL
- Browser-based usage
- Easy access for users

---

# 🌱 Future Enhancements

Future improvements planned:

- AI Resume Builder
- Resume Analysis System
- Interview Preparation Module
- Skill Gap Analysis
- Course Recommendation System
- Career Progress Tracking
- Multi-language Support
- Advanced AI Mentor Features

---

# 🎯 Project Highlights

This project demonstrates practical implementation of:

- Generative AI
- Google Gemini API Integration
- Prompt Engineering
- Streamlit Web Application Development
- Database Management
- User Authentication
- PDF Automation
- AI-Based Career Guidance System

---

# 👩‍💻 Developer

Developed by:

Yashasri

Project:

AI Career Roadmap Generator

Technology Stack:

Python, Streamlit, Google Gemini AI, SQLite, ReportLab

---

# 📜 License

This project is developed for educational and learning purposes.

Users can study and improve this project while giving proper credit to the original developer.

---

# ⭐ Acknowledgement

Special thanks to:

- Google Gemini AI
- Streamlit Community
- Python Open Source Community

for providing powerful technologies and tools for building this application.

---

© 2026 AI Career Roadmap Generator