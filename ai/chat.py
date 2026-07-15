import google.generativeai as genai

def career_chat(user_question, career_goal, qualification, skills):
    prompt = f"""
You are a friendly AI Career Mentor.

Career Goal: {career_goal}
Qualification: {qualification}
Skills: {skills}

The user asked:
{user_question}

Reply in simple English.
Keep the answer short (5-8 lines).
Give practical career advice.
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return response.text