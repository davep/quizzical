"""Provides code for working with quiz parameters."""

##############################################################################
# Python imports.
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, cast

##############################################################################
# Local imports.
from ...opentdb import Difficulty, Type


##############################################################################
class QuizTimer(Enum):
    """The types of timer a quiz can have."""

    NONE = 0
    """No timer."""

    PER_QUESTION = 1
    """Timer per question."""

    WHOLE_QUIZ = 2
    """Timer for whole quiz."""

    @property
    def description(self) -> str:
        """The description of the timer type."""
        return cast(
            dict[QuizTimer, str],
            {
                self.NONE: "No Timer",
                self.PER_QUESTION: "Seconds per question",
                self.WHOLE_QUIZ: "Seconds for the whole quiz",
            },
        )[self]


##############################################################################
@dataclass
class QuizParameters:
    """Holds the chosen parameters for making a quiz."""

    title: str
    """The title for the quiz."""

    number_of_questions: int = 10
    """The number of questions in the quiz."""

    category: int | None = None
    """The category for the quiz."""

    difficulty: Difficulty | None = None
    """The difficulty for the quiz."""

    question_type: Type | None = None
    """The type of question to ask."""

    timer_type: QuizTimer = QuizTimer.NONE
    """The type of timer to use for the quiz."""

    timer_value: int = 0
    """The number of seconds for the timer, if there is one."""

    def __post_init__(self) -> None:
        """Tidy up the data post-init."""
        # If we've been pulled in from a JSON source, it's likely that we
        # got the timer type back as an integer; to save a lot of cocking
        # about with decoders and stuff, let's just cast it here.
        self.timer_type = QuizTimer(self.timer_type)

    @property
    def as_json(self) -> dict[str, Any]:
        """The quiz parameters as a JSON-friendly dictionary."""
        return asdict(self)


### quiz_parameters.py ends here
