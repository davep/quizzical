"""Provides code for working with quiz parameters."""

##############################################################################
# Python imports.
from dataclasses import dataclass

##############################################################################
# Local imports.
from ...opentdb import Category, Difficulty, Type


##############################################################################
@dataclass
class QuizParameters:
    """Holds the chosen parameters for making a quiz."""

    title: str
    """The title for the quiz."""

    number_of_questions: int = 10
    """The number of questions in the quiz."""

    category: Category | None = None
    """The category for the quiz."""

    difficulty: Difficulty | None = None
    """The difficulty for the quiz."""

    question_type: Type | None = None
    """The type of question to ask."""


### quiz_parameters.py ends here
