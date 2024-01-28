"""Provides a widget for displaying a set of answers."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from functools import partial

##############################################################################
# Textual imports.
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import var

##############################################################################
# Local imports.
from ...opentdb import Question
from .answer import Answer


##############################################################################
class Answers(Vertical, can_focus=True):
    """Displays and a collection of answers and prompts for one."""

    DEFAULT_CSS = """
    Answers {
        height: auto;
        opacity: 0.5;
        border-top: dashed $primary;
        border-bottom: dashed $primary;
        margin: 0 2 1 2;

        &:focus {
            opacity: 1;
            background: $boost;
        }

        Answer.sep {
            border-top: dashed $primary;
        }

        Answer.correct * {
            background: $success 50%;
        }

        Answer.incorrect * {
            background: $error 50%;
        }
    }
    """

    BINDINGS = [((str(n), f"answer({n})")) for n in range(1, 5)]

    question: var[Question | None] = var(None, init=False)
    """The question whose answers are to be shown."""

    @dataclass
    class Given(Message):
        """Base class for the given answer."""

        answer: str | None = None
        """The answer that was given."""

    class Correct(Given):
        """Message sent when the player gives a correct answer."""

    class Incorrect(Given):
        """message sent when the player gives an incorrect answer."""

    answer: var[Given | None] = var(None)
    """The answer being processed."""

    async def _watch_question(self) -> None:
        """React to a new question being set."""
        await self.query(Answer).remove()
        if self.question is not None:
            await self.mount_all(
                Answer(question, number + 1, classes=("sep" if number else ""))
                for number, question in enumerate(self.question.answers)
            )
            self.answer = None

    def action_answer(self, answer: int) -> None:
        """Process a player's answer.

        Args:
            answer: The answer given by the player.
        """
        if self.question is None or self.answer is not None:
            return
        self.answer = (
            self.Correct
            if self.question.correct_answer == self.question.answers[answer - 1]
            else self.Incorrect
        )(self.question.answers[answer - 1])
        self.query_one(f"#answer-{answer}").set_class(
            True, "correct" if isinstance(self.answer, self.Correct) else "incorrect"
        )
        self.set_timer(0.6, partial(self.post_message, self.answer))

    def skip_question(self) -> None:
        """Skip the current question."""
        self.query(Answer).set_class(True, "incorrect")
        self.set_timer(0.6, partial(self.post_message, self.Incorrect()))


### answers.py ends here
