"""Provides code for working with quiz parameters."""

##############################################################################
# Python imports.
from dataclasses import asdict, dataclass
from typing import Any

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

    @property
    def as_json(self) -> dict[str, Any]:
        """The quiz parameters as a JSON-friendly dictionary."""
        return asdict(self)


### quiz_parameters.py ends here
