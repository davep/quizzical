"""The main screen of the application."""

##############################################################################
# Textual imports.
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Label

##############################################################################
# Local imports.
from ... import __version__
from ...opentdb import OpenTriviaDB
from ..widgets import Logo, QuestionCounts, QuizList
from .quiz_maker import QuizMaker


##############################################################################
class Main(Screen):
    """The main screen of the application."""

    CSS = """
    #version {
        width: 1fr;
        content-align: center middle;
        background: $primary;
        padding-bottom: 1;
    }

    QuizList {
        border-top: solid $boost;
        background: $primary;
    }

    #buttons {
        height: auto;
        background: $primary;
        border-top: solid $boost;
        padding-bottom: 1;
        Button {
            width: 1fr;
            margin: 0 1 0 1;
        }
    }
    """

    BINDINGS = [
        Binding("r", "run", "Run"),
        Binding("n", "new", "New"),
        Binding("e", "edit", "Edit"),
        Binding("d", "delete", "Delete"),
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

    def on_mount(self) -> None:
        """Load up the data for the main display."""
        self._load_counts()

    @work
    async def _load_counts(self) -> None:
        """Load up the question counts."""
        self.query_one(QuestionCounts).counts = await self._trivia.overall_counts()

    @on(Button.Pressed, "#run")
    def action_run(self) -> None:
        """Run the currently-hilighted quiz."""
        self.notify("TODO")

    @on(Button.Pressed, "#new")
    @work
    async def action_new(self) -> None:
        """Create a new quiz."""
        if quiz := await self.app.push_screen_wait(
            QuizMaker(await self._trivia.categories())
        ):
            self.notify(f"{quiz!r}")

    @on(Button.Pressed, "#edit")
    def action_edit(self) -> None:
        """Edit the currently-highlighted quiz."""
        self.notify("TODO")

    @on(Button.Pressed, "#delete")
    def action_delete(self) -> None:
        """Delete the currently-highlighted quiz."""
        self.notify("TODO")


### main.py ends here
