"""Provides a class that holds questions pulled from the API."""

##############################################################################
# Python imports.
from dataclasses import dataclass, field
from html import unescape

from typing_extensions import Literal

##############################################################################
Type = Literal["multiple", "boolean"]
"""The valid types of question."""

##############################################################################
Difficulty = Literal["easy", "medium", "hard"]
"""The valid question difficulty levels."""


##############################################################################
@dataclass
class Question:
    """Holds the details of a question."""

    type: Type
    """The type of the question."""

    difficulty: Difficulty
    """The difficulty level of the question."""

    category: str
    """The name of the category that the question is within."""

    question: str
    """The question itself."""

    correct_answer: str
    """The correct answer to the question."""

    incorrect_answers: list[str] = field(default_factory=list)
    """The incorrect answers for the question."""

    def __post_init__(self) -> None:
        """Tidy up the question data once it's been loaded up."""
        self.category = unescape(self.category)
        self.question = unescape(self.question)
        self.correct_answer = unescape(self.correct_answer)
        self.incorrect_answers = [unescape(answer) for answer in self.incorrect_answers]

    @property
    def answers(self) -> list[str]:
        """All of the answers to the question, sorted in alphabetical order."""
        return sorted([self.correct_answer, *self.incorrect_answers], key=str.casefold)


### question.py ends here
