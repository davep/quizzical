"""The main screen of the application."""

##############################################################################
# Textual imports.
from textual import work
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header

##############################################################################
# Local imports.
from ... import __version__
from ...opentdb import OpenTriviaDB
from ..widgets import Logo, QuestionCounts


##############################################################################
class Main(Screen):
    """The main screen of the application."""

    SUB_TITLE = f"v{__version__}"

    CSS = """
    Header {
        HeaderIcon {
            visibility: hidden;
        }

        &.-tall {
            height: 1;
        }
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._trivia = OpenTriviaDB()
        """The Open Trivia DB client."""

    def compose(self) -> ComposeResult:
        """Compose the main screen."""
        yield Header()
        yield Logo()
        yield QuestionCounts("All Questions")
        yield Footer()

    def on_mount(self) -> None:
        """Load up the data for the main display."""
        self._load_counts()

    @work
    async def _load_counts(self) -> None:
        """Load up the question counts."""
        self.query_one(QuestionCounts).counts = await self._trivia.overall_counts()


### main.py ends here
