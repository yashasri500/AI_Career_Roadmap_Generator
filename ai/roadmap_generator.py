"""
Gemini AI Roadmap Generator
"""

import google.generativeai as genai

from ai.prompts import build_career_prompt


def generate_career_roadmap(
    full_name,
    qualification,
    skills,
    career_goal
):
    """
    Generate personalized AI career report.
    """

    prompt = build_career_prompt(
        full_name,
        qualification,
        skills,
        career_goal
    )

    try:

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(
            prompt
        )
        print(repr(response.text))

        return response.text

    except Exception as e:

        raise e