"""Modal dialog for getting the parameters to make a quiz."""

##############################################################################
# Python imports.
from dataclasses import dataclass
from typing import cast, get_args

##############################################################################
# Textual imports.
from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.validation import Integer, Length
from textual.widgets import Button, Input, Label, Select

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


##############################################################################
class QuizMaker(ModalScreen[QuizParameters | None]):
    """Modal screen for prompting the user for quiz parameters."""

    DEFAULT_CSS = """
    QuizMaker {
        align: center middle;

        &> Vertical {
            width: 70%;
            height: auto;
            background: $surface;
            border: panel $primary;
            border-title-color: $accent;

            Label {
                margin: 1 0 0 1;
            }

            &> Horizontal {
                margin-top: 1;
                height: auto;
                align: right middle;
                Button {
                    margin-left: 1;
                }
            }
        }
    }
    """

    BINDINGS = [("escape", "cancel"), ("f2", "okay")]

    def __init__(self, categories: list[Category]) -> None:
        super().__init__()
        self._categories = categories
        """The known categories for the questions."""

    def compose(self) -> ComposeResult:
        """Compose the content of the dialog."""
        with Vertical() as dialog:
            dialog.border_title = "Quiz Options"
            yield Label("Title:")
            yield Input(
                placeholder="The title for the quiz",
                validators=Length(minimum=1),
                id="title",
            )
            yield Label("Number of questions:")
            yield Input(
                "10",
                placeholder="Number of questions to ask",
                type="integer",
                validators=Integer(minimum=1),
                id="number",
            )
            yield Label("Category:")
            yield Select[int](
                ((category.name, category.id) for category in self._categories),
                prompt="Any Category",
                id="category",
            )
            yield Label("Difficulty:")
            yield Select[str](
                (
                    (difficulty.capitalize(), difficulty)
                    for difficulty in get_args(Difficulty)
                ),
                prompt="Any Difficulty",
                id="difficulty",
            )
            yield Label("Question Type:")
            yield Select[str](
                (
                    (
                        "Multiple Choice"
                        if question_type == "multiple"
                        else "True or False",
                        question_type,
                    )
                    for question_type in get_args(Type)
                ),
                prompt="Any Type",
                id="type",
            )
            with Horizontal():
                yield Button("Okay [dim]\\[F2][/]", id="okay")
                yield Button("Cancel [dim]\\[Esc][/]", id="cancel")

    @on(Button.Pressed, "#okay")
    def action_okay(self) -> None:
        """React to the user confirming their choices."""
        okay = True
        if not (okay := okay and self.query_one("#title", Input).is_valid):
            self.notify("Please enter a title", title="Missing Title", severity="error")
        if not (okay := okay and self.query_one("#number", Input).is_valid):
            self.notify(
                "Please enter a valid number", title="Invalid Number", severity="error"
            )
        if okay:
            self.dismiss(
                QuizParameters(
                    title=self.query_one("#title", Input).value,
                    number_of_questions=int(self.query_one("#number", Input).value),
                    category=(
                        self._categories[category]
                        if isinstance(
                            category := self.query_one("#category", Select).value, int
                        )
                        else None
                    ),
                    difficulty=(
                        cast(Difficulty, difficulty)
                        if isinstance(
                            difficulty := self.query_one("#difficulty", Select).value,
                            str,
                        )
                        else None
                    ),
                    question_type=(
                        cast(Type, question_type)
                        if isinstance(
                            question_type := self.query_one("#type", Select).value, str
                        )
                        else None
                    ),
                )
            )

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """React to the user cancelling their choices."""
        self.dismiss(None)


### quiz_maker.py ends here
