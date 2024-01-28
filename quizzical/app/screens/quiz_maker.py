"""Modal dialog for getting the parameters to make a quiz."""

##############################################################################
# Python imports.
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
from ..data import QuizParameters, QuizTimer


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
                &:disabled {
                    color: $text-muted;
                }
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

    def __init__(
        self, categories: list[Category], quiz: QuizParameters | None = None
    ) -> None:
        """Initialise the quiz maker.

        Args:
            categories: The list of categories that the user can select from.
            quiz: An optional existing quiz to populate the dialog with.
        """
        super().__init__()
        self._categories = categories
        """The known categories for the questions."""
        self._quiz = quiz
        """Existing quiz parameters to populate the list with."""

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
            yield Label("Timer Type:")
            yield Select[QuizTimer](
                ((timer.description, timer) for timer in list(QuizTimer)),
                value=QuizTimer.NONE,
                allow_blank=False,
                id="timer-type",
            )
            yield Label("Timer Seconds:", classes="timer", disabled=True)
            yield Input(
                "30",
                placeholder="Number of seconds for the timer",
                type="integer",
                validators=Integer(minimum=1),
                id="timer-seconds",
                classes="timer",
                disabled=True,
            )
            with Horizontal():
                yield Button("Okay [dim]\\[F2][/]", id="okay")
                yield Button("Cancel [dim]\\[Esc][/]", id="cancel")

    def on_mount(self) -> None:
        """Configure the dialog once the DOM is ready."""
        if self._quiz is not None:
            self.query_one("#title", Input).value = self._quiz.title
            self.query_one("#number", Input).value = str(self._quiz.number_of_questions)
            self.query_one("#category", Select).value = (
                self._quiz.category if self._quiz.category else Select.BLANK
            )
            self.query_one("#difficulty", Select).value = (
                self._quiz.difficulty or Select.BLANK
            )
            self.query_one("#type", Select).value = (
                self._quiz.question_type or Select.BLANK
            )
            self.query_one("#timer-type", Select).value = self._quiz.timer_type
            self.query_one("#timer-seconds", Input).value = str(self._quiz.timer_value)
            self._update_timer_fields()

    @on(Select.Changed, "#timer-type")
    def _update_timer_fields(self) -> None:
        """Refresh the state of the timer input fields."""
        timer_type = self.query_one("#timer-type", Select).value
        for widget in self.query(".timer").results():
            widget.disabled = timer_type == QuizTimer.NONE
            if isinstance(widget, Input):
                if widget.disabled:
                    widget.validators = []
                else:
                    widget.validators = [Integer(minimum=1)]
                widget.validate(widget.value)

    @on(Button.Pressed, "#okay")
    def action_okay(self) -> None:
        """React to the user confirming their choices."""
        okay = True
        if not self.query_one("#title", Input).is_valid:
            self.notify("Please enter a title", title="Missing Title", severity="error")
            okay = False
        if not self.query_one("#number", Input).is_valid:
            self.notify(
                "Please enter a valid number", title="Invalid Number", severity="error"
            )
            okay = False
        timer_seconds = self.query_one("#timer-seconds", Input)
        if not timer_seconds.disabled:
            if not timer_seconds.is_valid:
                self.notify(
                    "Please enter a valid number of seconds for the timer",
                    title="Invalid Timer",
                    severity="error",
                )
                okay = False
        if okay:
            self.dismiss(
                QuizParameters(
                    title=self.query_one("#title", Input).value,
                    number_of_questions=int(self.query_one("#number", Input).value),
                    category=category
                    if isinstance(
                        category := self.query_one("#category", Select).value, int
                    )
                    else None,
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
                    timer_type=(
                        timer_type
                        if isinstance(
                            timer_type := self.query_one("#timer-type", Select).value,
                            QuizTimer,
                        )
                        else QuizTimer.NONE
                    ),
                    timer_value=int(
                        self.query_one("#timer-seconds", Input).value or "0"
                    ),
                )
            )

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        """React to the user cancelling their choices."""
        self.dismiss(None)


### quiz_maker.py ends here
