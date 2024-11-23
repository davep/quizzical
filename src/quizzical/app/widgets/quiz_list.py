"""Provides a widget that holds the list of saved quiz parameters."""

##############################################################################
# Backward compatibility.
from __future__ import annotations

##############################################################################
# Python imports.
from dataclasses import dataclass
from json import dumps, loads

##############################################################################
# Textual imports.
from textual import on
from textual.events import Mount
from textual.message import Message
from textual.reactive import var
from textual.widgets import OptionList

##############################################################################
# Backward-compatible typing.
from typing_extensions import Self

##############################################################################
# Local imports.
from ..data import QuizParameters, quizzes_file


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

    BINDINGS = [
        ("s, j, right", "cursor_down"),
        ("w, k, left", "cursor_up"),
    ]

    quizzes: var[list[QuizParameters]] = var(list, always_update=True, init=False)
    """The list of all the quiz parameters."""

    @dataclass
    class Changed(Message):
        """Message sent when the quiz list has been changed."""

        quiz_list: QuizList
        """The quiz list that was changed."""

    def _changed(self) -> None:
        """Handle the list being changed."""
        quizzes_file().write_text(
            dumps(
                [quiz.as_json for quiz in self.quizzes],
                indent=4,
                default=lambda x: x.value,
            ),
            encoding="utf-8",
        )
        self.post_message(self.Changed(self))

    @on(Mount)
    def _load(self) -> None:
        """Load the current quiz list."""
        try:
            self.quizzes = [
                QuizParameters(**quiz)
                for quiz in loads(quizzes_file().read_text(encoding="utf-8"))
            ]
        except FileNotFoundError:
            pass
        else:
            self.post_message(self.Changed(self))

    def _watch_quizzes(self) -> None:
        """Refresh the prompt list when the quiz list is reassigned."""
        self.clear_options().add_options([quiz.title for quiz in self.quizzes])
        if self.quizzes:
            self.highlighted = 0

    def add_quiz(self, quiz: QuizParameters) -> None:
        """Add a new quiz to the list.

        Args:
            quiz: The quiz parameters to add.
        """
        self.add_option(quiz.title)
        self.quizzes.append(quiz)
        if self.highlighted is None:
            self.highlighted = 0
        self._changed()

    def modify_quiz(self, index: int, quiz: QuizParameters) -> None:
        """Modify the given quiz with the new parameters.

        Args:
            index: The index of the quiz to update.
            quiz: The quiz parameters to replace the quiz with.
        """
        self.quizzes[index] = quiz
        self.replace_option_prompt_at_index(index, quiz.title)
        self._changed()

    def remove_quiz(self, index: int) -> None:
        """Remove the quiz at the given index.

        Args:
            index: The index of the quiz to remove.
        """
        del self.quizzes[index]
        self.remove_option_at_index(index)
        self._changed()


### quiz_list.py ends here
