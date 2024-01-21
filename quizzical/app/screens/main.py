"""The main screen of the application."""

##############################################################################
# Textual imports.
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header

##############################################################################
# Local imports.
from ... import __version__
from ..widgets import Logo


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

    def compose(self) -> ComposeResult:
        """Compose the main screen."""
        yield Header()
        yield Logo()
        yield Footer()


### main.py ends here
