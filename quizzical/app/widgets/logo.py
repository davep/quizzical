"""Provides a logo widget."""

##############################################################################
# Textual imports.
from textual.app import RenderResult
from textual.geometry import Size
from textual.widget import Widget

##############################################################################
LOGO = r""" ____   ____   ____   ____   ____   ____   ____   ____   ____
||Q || ||u || ||i || ||z || ||z || ||i || ||c || ||a || ||l ||
||__|| ||__|| ||__|| ||__|| ||__|| ||__|| ||__|| ||__|| ||__||
|/__\| |/__\| |/__\| |/__\| |/__\| |/__\| |/__\| |/__\| |/__\|
"""


##############################################################################
class Logo(Widget):
    """The logo for the application."""

    DEFAULT_CSS = """
    Logo {
        width: 1fr;
        height: auto;
        content-align: center middle;
        color: $warning;
        background: $primary;
        padding-bottom:1 ;
    }
    """

    def render(self) -> RenderResult:
        """Render the logo."""
        return LOGO

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:
        del container, viewport, width
        return 4


### logo.py ends here
