"""Provides a widget that holds the list of saved quiz parameters."""

##############################################################################
# Textual imports.
from textual.widgets import OptionList
from textual.widgets.option_list import Option


##############################################################################
class Quiz(Option):
    """Holds the details of a quiz."""


##############################################################################
class QuizList(OptionList):
    """Holds the list of available quizzes."""

    DEFAULT_CSS = """
    QuizList {
        height: 1fr;
        border: none;

        &:focus {
            border: none;
            background: $boost;
        }
    }
    """


### quiz_list.py ends here
