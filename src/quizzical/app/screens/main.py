"""The main screen of the application."""

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Label

##############################################################################
# Local imports.
from ... import __version__
from ...opentdb import OpenTriviaDB
from ..widgets import Logo, QuestionCounts, QuizList
from .confirm import Confirm
from .quiz_maker import QuizMaker
from .quiz_taker import QuizTaker


##############################################################################
class Main(Screen[None]):
    """The main screen of the application."""

    CSS = """
    #version {
        width: 1fr;
        content-align: center middle;
        padding-bottom: 1;
    }

    QuizList {
        border-top: solid $boost;
    }

    #buttons {
        height: auto;
        border-top: solid $boost;
        padding-bottom: 1;
        Button {
            width: 1fr;
            min-width: 0;
            margin: 0 1 0 1;
        }
    }
    """

    BINDINGS = [
        ("r", "run"),
        ("n", "new"),
        ("e", "edit"),
        ("d", "delete"),
        ("q", "quit"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._trivia = OpenTriviaDB()
        """The Open Trivia DB client."""

    def compose(self) -> ComposeResult:
        """Compose the main screen."""
        yield Logo()
        yield Label(f"v{__version__}", id="version")
        yield QuestionCounts("All Questions")
        yield QuizList()
        with Horizontal(id="buttons"):
            yield Button("Run [dim]\\[r][/]", id="run", disabled=True)
            yield Button("New [dim]\\[n][/]", id="new")
            yield Button("Edit [dim]\\[e][/]", id="edit", disabled=True)
            yield Button("Delete [dim]\\[d][/]", id="delete", disabled=True)
            yield Button("Quit [dim]\\[q][/]", id="quit")

    def on_mount(self) -> None:
        """Load up the data for the main display."""
        self._load_counts()

    def _connect_error(self) -> None:
        """Let the user know there was an error when connecting to the backend."""
        self.notify(
            "Unable to connect to https://opentdb.com/ at the moment!",
            severity="error",
            timeout=8,
        )
        self.query_one("#buttons").disabled = True

    @work
    async def _load_counts(self) -> None:
        """Load up the question counts."""
        try:
            self.query_one(QuestionCounts).counts = await self._trivia.overall_counts()
        except self._trivia.RequestError:
            self.query_one(QuestionCounts).counts = QuestionCounts.Unavailable()
            self._connect_error()

    @on(QuizList.Changed)
    def _update_buttons(self, event: QuizList.Changed) -> None:
        """Update the state of the buttons.

        Args:
            event: The event to handle.
        """
        self.query_one("#run").disabled = event.quiz_list.highlighted is None
        self.query_one("#edit").disabled = event.quiz_list.highlighted is None
        self.query_one("#delete").disabled = event.quiz_list.highlighted is None

    @on(Button.Pressed, "#run")
    def action_run(self) -> None:
        """Run the currently-hilighted quiz."""
        quizzes = self.query_one(QuizList)
        if quizzes.highlighted is not None:
            self.app.push_screen(
                QuizTaker(self._trivia, quizzes.quizzes[quizzes.highlighted])
            )

    @on(Button.Pressed, "#new")
    @work
    async def action_new(self) -> None:
        """Create a new quiz."""
        try:
            if quiz := await self.app.push_screen_wait(
                QuizMaker(await self._trivia.categories())
            ):
                self.query_one(QuizList).add_quiz(quiz)
        except self._trivia.RequestError:
            self._connect_error()

    @on(Button.Pressed, "#edit")
    @work
    async def action_edit(self) -> None:
        """Edit the currently-highlighted quiz."""
        quizzes = self.query_one(QuizList)
        if (to_edit := quizzes.highlighted) is not None:
            try:
                if quiz := await self.app.push_screen_wait(
                    QuizMaker(await self._trivia.categories(), quizzes.quizzes[to_edit])
                ):
                    quizzes.modify_quiz(to_edit, quiz)
            except self._trivia.RequestError:
                self._connect_error()

    @on(Button.Pressed, "#delete")
    @work
    async def action_delete(self) -> None:
        """Delete the currently-highlighted quiz."""
        if (to_delete := self.query_one(QuizList).highlighted) is not None:
            if await self.app.push_screen_wait(
                Confirm("Delete Quiz", "Are you sure you want to delete that quiz?")
            ):
                self.query_one(QuizList).remove_quiz(to_delete)

    @on(Button.Pressed, "#quit")
    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()


### main.py ends here
