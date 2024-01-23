"""Provides the screen used to take a quiz."""

##############################################################################
# Textual imports.
from textual import work
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, LoadingIndicator, Pretty

##############################################################################
# Local imports.
from ...opentdb import OpenTriviaDB, Question
from ..data.quiz_parameters import QuizParameters


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

        #taker {
            width: 80%;
            height: 80%;
        }
    }
    """

    def __init__(self, client: OpenTriviaDB, quiz: QuizParameters) -> None:
        super().__init__()
        self._client = client
        """The trivia database client object."""
        self._quiz_parameters = quiz
        """The parameters of the quiz we're going to take."""
        self._quiz = list[Question]

    def compose(self) -> ComposeResult:
        """Compose the quiz taking screen."""

        with Vertical(id="loader") as quiz_loader:
            quiz_loader.border_title = f"Loading: {self._quiz_parameters.title}"
            yield LoadingIndicator()
            with Center():
                yield Button("Cancel")  # TODO

        with Vertical(id="taker", classes="hidden") as quiz_taker:
            quiz_taker.border_title = self._quiz_parameters.title
            yield Pretty([])
            with Center():
                yield Button("Worked")

    def on_mount(self) -> None:
        """Start the process of loading up the quiz once the DOM is ready."""
        self._load_quiz()

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
            self.query_one("#taker").set_class(False, "hidden")
            self.query_one(Pretty).update(self._quiz)


### quiz_taker.py ends here
