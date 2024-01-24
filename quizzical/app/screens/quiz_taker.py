"""Provides the screen used to take a quiz."""

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Center, Grid, Vertical
from textual.css.query import NoMatches
from textual.reactive import var
from textual.screen import ModalScreen
from textual.widgets import Button, Digits, Label, LoadingIndicator, RadioSet

##############################################################################
# Local imports.
from ...opentdb import OpenTriviaDB, Question
from ..data.quiz_parameters import QuizParameters, QuizTimer


##############################################################################
class QuizTaker(ModalScreen):
    """Screen for taking a quiz."""

    DEFAULT_CSS = """
    QuizTaker {
        align: center middle;

        .hidden {
            display: none;
        }

        &> Vertical {
            background: $surface;
            border: panel $primary;
            border-title-color: $accent;
        }

        #loader {
            width: 30%;
            min-width: 50;
            height: auto;
            LoadingIndicator {
               height: 3;
            }
        }

        #confirmer {
            padding: 1 1 0 1;
            width: auto;
            height: auto;
            Label {
                width: auto;
                margin-bottom: 1;
                text-align: center;
            }
            Center {
                width: 100%;
                layout: horizontal;
            }
            Button {
                margin-right: 1;
            }
        }

        #taker {
            width: auto;
            max-width: 60;
            height: auto;

            Grid {
                grid-size: 4 2;
                height: auto;
                grid-rows: auto;
                Label, Digits {
                    width: 1fr;
                    text-align: center;
                }
            }

            #question-text {
                width: 1fr;
                height: auto;
                padding: 2;
                text-style: bold;
            }

            #answers {
                width: 1fr;
                border: none;
                margin: 0 1 1 1;
                padding: 1;
                &:focus {
                    border: none;
                }
            }
        }
    }
    """

    _question: var[int] = var(0, init=False)
    """The number of the question being asked."""

    _answers: var[list[str]] = var(list, init=False)
    """Holds the answers given."""

    _correct: var[int] = var(0, init=False)
    """The count of correct answers."""

    _wrong: var[int] = var(0, init=False)
    """The count of wrong answers."""

    def __init__(self, client: OpenTriviaDB, quiz: QuizParameters) -> None:
        """Initialise the quiz taking screen.

        Args:
            client: The API client.
            quiz: The parameters for the quiz to take.
        """
        super().__init__()
        self._client = client
        """The trivia database client object."""
        self._quiz_parameters = quiz
        """The parameters of the quiz we're going to take."""
        self._quiz: list[Question] = []

    def compose(self) -> ComposeResult:
        """Compose the quiz taking screen."""

        with Vertical(id="loader") as quiz_loader:
            quiz_loader.border_title = f"Loading: {self._quiz_parameters.title}"
            yield LoadingIndicator()
            with Center():
                yield Button("Cancel", id="cancel")

        with Vertical(id="confirmer", classes="hidden") as quiz_confirmer:
            quiz_confirmer.border_title = (
                f"Ready to take '{self._quiz_parameters.title}'?"
            )
            yield Label("The quiz is now loaded and ready; are you all set to take it?")
            with Center():
                yield Label(id="details")
            with Center():
                yield Button("Let's go!", id="take", variant="success")
                yield Button("Cancel", id="cancel", variant="error")

        with Vertical(id="taker", classes="hidden") as quiz_taker:
            quiz_taker.border_title = self._quiz_parameters.title
            with Grid():
                yield Label("Question")
                yield Label("Out Of")
                yield Label("Correct")
                yield Label("Wrong")
                yield Digits("0", id="question")
                yield Digits("0", id="out-of")
                yield Digits("0", id="correct")
                yield Digits("0", id="wrong")
            yield Label(id="question-text")
            with Center():
                yield Button("Cancel", id="cancel")

    def on_mount(self) -> None:
        """Start the process of loading up the quiz once the DOM is ready."""
        self._load_quiz()

    async def _quiz_summary(self) -> str:
        """A descriptive summary of the quiz."""
        summary = f"{len(self._quiz)} question{'' if len(self._quiz) == 1 else 's'}\n"
        if self._quiz_parameters.category is None:
            summary += "Any category\n"
        else:
            summary += f"{(await self._client.category(self._quiz_parameters.category)).name}\n"
        if self._quiz_parameters.difficulty is None:
            summary += "Any difficulty level\n"
        else:
            summary += (
                f"{self._quiz_parameters.difficulty.capitalize()} difficulty level\n"
            )
        if self._quiz_parameters.question_type is None:
            summary += "Multiple choice and true/false questions\n"
        else:
            summary += f"{'True or false' if self._quiz_parameters.question_type == 'boolean' else 'Multiple choice'} questions\n"
        if self._quiz_parameters.timer_type == QuizTimer.PER_QUESTION:
            summary += f"{self._quiz_parameters.timer_value} seconds per question\n"
        if self._quiz_parameters.timer_type == QuizTimer.WHOLE_QUIZ:
            summary += (
                f"{self._quiz_parameters.timer_value} seconds to complete the quiz\n"
            )
        return summary

    @work
    async def _load_quiz(self) -> None:
        """Load the quiz from the backend."""
        self._quiz = await self._client.questions(
            amount=self._quiz_parameters.number_of_questions,
            category=self._quiz_parameters.category,
            difficulty=self._quiz_parameters.difficulty,
            type=self._quiz_parameters.question_type,
        )
        with self.app.batch_update():
            self.query_one("#loader").set_class(True, "hidden")
            self.query_one("#confirmer").set_class(False, "hidden")
            self.query_one("#taker").set_class(True, "hidden")
            self.query_one("#confirmer #details", Label).update(
                await self._quiz_summary()
            )
            self.query_one("#take").focus()

    async def _watch__question(self) -> None:
        self.query_one("#question", Digits).update(str(self._question))
        self.query_one("#question-text", Label).update(
            self._quiz[self._question - 1].question
        )
        try:
            await self.query_one("#answers").remove()
        except NoMatches:
            pass
        await self.query_one("#taker").mount(
            RadioSet(
                *[answer for answer in self._quiz[self._question - 1].answers],
                id="answers",
            ),
            after="#question-text",
        )

    def _watch__correct(self) -> None:
        self.query_one("#correct", Digits).update(str(self._correct))

    def _watch__wrong(self) -> None:
        self.query_one("#wrong", Digits).update(str(self._wrong))

    @on(Button.Pressed, "#cancel")
    def cancel_quiz(self) -> None:
        """Cancel the current quiz."""
        self.dismiss()

    @on(Button.Pressed, "#take")
    def take_quiz(self) -> None:
        with self.app.batch_update():
            self.query_one("#loader").set_class(True, "hidden")
            self.query_one("#confirmer").set_class(True, "hidden")
            self.query_one("#taker").set_class(False, "hidden")
            self.query_one("#out-of", Digits).update(str(len(self._quiz)))
            self._question = 1

    @on(RadioSet.Changed)
    def answered(self, event: RadioSet.Changed) -> None:
        question = self._quiz[self._question - 1]
        if question.correct_answer == question.answers[event.index]:
            self._correct += 1
        else:
            self._wrong += 1
        self._answers.append(self._quiz[self._question - 1].answers[event.index])
        self._question += 1


### quiz_taker.py ends here
