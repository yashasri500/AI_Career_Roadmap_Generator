from dataclasses import dataclass


@dataclass
class User:
    """
    User model.
    """

    username: str
    password: str
    created_at: str


@dataclass
class CareerProfile:
    """
    Career profile entered by the user.
    """

    full_name: str
    qualification: str
    skills: str
    career_goal: str


@dataclass
class RoadmapHistory:
    """
    Saved roadmap history model.
    """

    username: str
    full_name: str
    qualification: str
    skills: str
    career_goal: str
    generated_date: str