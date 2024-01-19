"""The main application class."""

##############################################################################
# Textual imports.
from textual.app import App

##############################################################################
# Local imports.
from .screens import Main


##############################################################################
class Quizzical(App[None]):
    """The Quizzical application."""

    ENABLE_COMMAND_PALETTE = False

    def on_mount(self) -> None:
        """Load up the main screen once the DOM is ready."""
        self.push_screen(Main())


### quizzical.py ends here
