
HELP_MESSAGE = """Commands:
⚪ /start – Start Bot
⚪ /vote – Vote for a project
⚪ /projects – List projects
⚪ /retract – Retract vote
⚪ /help – Show help message
"""

from typing import Final, TypedDict, List

class Menu(TypedDict):
    name: str
    callback_data: str


MENUS : List[Menu] = [
    {
        "name": "Vote",
        "callback_data": "show_voting_options"
    },
    {
        "name": "Projects",
        "callback_data": "projects"
    },
    {
        "name": "About Hackathon",
        "callback_data": "about"
    },
    {
        "name": "Status",
        "callback_data": "voting_status"
    }
]

class Project(TypedDict):
    id: str
    name: str
    description: str

projects : List[Project] = [
    {
        "id": "1",
        "name": "Project 1",
        "description": "This is a project description"
    },
    {
        "id": "2",
        "name": "Project 2",
        "description": "This is a project description"
    },
    {

        "id": "3",
        "name": "Project 3",
        "description": "This is a project description"
    },
    {
        "id": "4",
        "name": "Project 4",
        "description": "This is a project description"
    },
    {
        "id": "5",
        "name": "Project 5",
        "description": "This is a project description"
    },
    {
        "id": "6",
        "name": "Project 6",
        "description": "This is a project description"
    },
    {
        "id": "7",
        "name": "Project 7",
        "description": "This is a project description"
    },
    {
        "id": "8",
        "name": "Project 8",
        "description": "This is a project description"
    },
]


START_MESSAGE : Final ="""
🚀 Welcome to the A2SV Expo Bot! 🚀
We're thrilled to have you here! 🌍✨

What can you do?
🏆 Project Voting:
Vote for your favorite projects at the A2SV Expo! Your input helps recognize outstanding work. Select "Vote for Projects" to get started.

🔍 Explore A2SV:
Learn more about A2SV, its mission, and find important links. Discover how we're empowering African tech talent and fostering innovation.

🗣 Give Feedback:
Share your thoughts on the expo and projects. Your feedback is invaluable! Select "Give Feedback" to tell us about your experience.

Gear up for an electrifying adventure of innovation and teamwork! 🌟🚀
"""

PROJECTS_MESSAGE : Final = "🌟 We have 8 projects for you to vote on. Select a project to learn more about it and cast your vote. 🚀🌟"

VOTE_CLOSED : Final = False

ABOUT_HACKATHON_MESSAGE : Final = """
🚀 A2SV AI for Impact Hackathon 🚀

🌟 Attracted nearly 5,000 registrations from students across 1,000+ universities and high schools in 48 African countries.

🛠️ Generated 500+ project ideas, leading to 32 projects in the semi-finals.

🏆 $30K Prize Pool:

🥇 First Place
    $ 10,000

    Trip to Addis Ababa, including airfare, hotel, food and other expenses.

    Opportunity to pitch one's project idea to renowned tech individuals and venture capitalists.

    Certificate of achievement.

    Direct placement opportunity in the A2SV education cohort 6.

    Custom-designed A2SV swag.


🥈 Second Place
    $ 6,000

    Trip to Addis Ababa, including airfare, hotel, food and other expenses.

    Opportunity to pitch one's project idea to renowned tech individuals and venture capitalists.

    Certificate of achievement.

    Custom-designed A2SV swag.

🥉 Third Place
    $ 4,000

    Trip to Addis Ababa, including airfare, hotel, food and other expenses.

    Opportunity to pitch one's project idea to renowned tech individuals and venture capitalists.

    Certificate of achievement.
"""


THANKYOU_FOR_VOTING : Final = """
Thank you so much for voting,
"""