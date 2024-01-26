"""Provides a widget for displaying a set of answers."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Textual imports.
from textual.containers import Vertical
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
        border: blank;

        &:focus {
            border: solid $accent;
        }

        Answer.sep {
            border-top: dashed $primary;
        }
    }
    """

    question: var[Question | None] = var(None, init=False)
    """The question whose answers are to be shown."""

    async def _watch_question(self) -> None:
        """React to a new question being set."""
        await self.query(Answer).remove()
        if self.question is not None:
            await self.mount_all(
                Answer(question, number + 1, classes=("sep" if number else ""))
                for number, question in enumerate(self.question.answers)
            )


### answers.py ends here
