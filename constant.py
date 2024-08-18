
HELP_MESSAGE = """Commands:
⚪ /start – Start Bot
⚪ /vote – Vote for a project
⚪ /projects – List projects
⚪ /retract – Retract vote
⚪ /help – Show help message
"""


# define a type for the menus
# q: is there a way to type it like an interface so that it has to have a name key?
# a: yes, you can use a TypedDict
# q:  How
# a:  You can import TypedDict from typing
from typing import TypedDict, List

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


projects : List[Menu] = [
    {
        "name": "Project 1",
    },
    {
        "name": "Project 2",
    },
    {
        "name": "Project 3",
    },
    {
        "name": "Project 4",
    },
    {
        "name": "Project 5",
    },
    {
        "name": "Project 6",
    },
    {
        "name": "Project 7",
    },
    {
        "name": "Project 8",
    },
]