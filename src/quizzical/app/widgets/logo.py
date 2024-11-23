"""Provides a logo widget."""

##############################################################################
# Python imports.
from typing import Final

##############################################################################
# Textual imports.
from textual.app import RenderResult
from textual.geometry import Size
from textual.widget import Widget

##############################################################################
LOGO: Final[str] = r""" ____   ____   ____   ____   ____   ____   ____   ____   ____
||Q || ||u || ||i || ||z || ||z || ||i || ||c || ||a || ||l ||
||__|| ||__|| ||__|| ||__|| ||__|| ||__|| ||__|| ||__|| ||__||
|/__\| |/__\| |/__\| |/__\| |/__\| |/__\| |/__\| |/__\| |/__\|
"""
LOGO_MEDIUM: Final[str] = "\n\nQ u i z z i c a l"
LOGO_SMALL: Final[str] = "\n\nQuizzical"


##############################################################################
class Logo(Widget):
    """The logo for the application."""

    DEFAULT_CSS = """
    Logo {
        width: 1fr;
        height: auto;
        content-align: center middle;
        color: $warning;
        padding-bottom: 1;
    }
    """

    def render(self) -> RenderResult:
        """Render the logo."""
        if self.container_size.width < 20:
            return LOGO_SMALL
        if self.container_size.width < 65:
            return LOGO_MEDIUM
        return LOGO

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        del container, viewport, width
        return 4


### logo.py ends here
