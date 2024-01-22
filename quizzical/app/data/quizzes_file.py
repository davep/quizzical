"""Code relating to the file of quizzes."""

##############################################################################
# Python imports.
from pathlib import Path

##############################################################################
# Local imports.
from .locations import data_dir


##############################################################################
def quizzes_file() -> Path:
    """The path to the file that holds all the quizzes."""
    return data_dir() / "quizzes.json"


### quizzes_file.py ends here
