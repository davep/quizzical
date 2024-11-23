"""The main entry point for the application."""

##############################################################################
# Local imports.
from .app import Quizzical


##############################################################################
def run() -> None:
    """Run the application."""
    Quizzical().run()


##############################################################################
if __name__ == "__main__":
    run()

### __main__.py ends here
