"""Provides a widget for displaying an answer."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Digits, Label


##############################################################################
class Answer(Horizontal):
    """Display an answer to a question."""

    DEFAULT_CSS = """
    Answer {
        width: 1fr;
        height: auto;
        padding: 0 1 0 1;

        Digits {
            width: auto;
            height: auto;
            padding-right: 1;
            color: $success;
        }

        Label {
            width: 1fr;
            height: auto;
            min-height: 3;
            content-align: left middle;
        }
    }
    """

    def __init__(self, answer: str, number: int, classes: str | None = None) -> None:
        """Initialise the answer.

        Args:
            answer: The answer text.
            number: The number the user will use to select the answer.
            classes: The classes to apply to the widget.
        """
        super().__init__(id=f"answer-{number}", classes=classes)
        self._answer = answer
        """The answer to show."""
        self._number = number
        """The number of the answer."""

    def compose(self) -> ComposeResult:
        """Compose the answer widget's content."""
        yield Digits(f"{self._number}:")
        yield Label(self._answer)


### answer.py ends here
