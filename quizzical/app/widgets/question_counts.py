"""Provides a widget that shows question count totals."""

##############################################################################
# Rich imports.
from rich.align import Align
from rich.console import Group
from rich.table import Table

##############################################################################
# Textual imports.
from textual.app import RenderResult
from textual.reactive import reactive
from textual.widget import Widget

##############################################################################
# Local imports.
from ...opentdb import Counts


##############################################################################
class QuestionCounts(Widget):
    """Widget that shows question counts."""

    DEFAULT_CSS = """
    QuestionCounts {
        height: auto;
        width: 1fr;
        background: $primary;
        color: $text-muted;
    }
    """

    counts: reactive[Counts] = reactive(Counts(0, 0, 0, 0))
    """The counts to show."""

    def __init__(
        self,
        title: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialise the question counts widget.

        Args:
            title: The title of the counts to show.
            name: The name of the question counts widget.
            id: The ID of the question counts widget in the DOM.
            classes: The CSS classes of the question counts widget.
            disabled: Whether the question counts widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self._title = title
        """The title of the counts."""

    def render(self) -> RenderResult:
        """Render the content of the widget."""
        display = Table(expand=True)
        for title in ("Total", "Pending", "Verified", "Rejected"):
            display.add_column(title, no_wrap=True, justify="right")
        display.add_row(
            str(self.counts.questions),
            str(self.counts.pending),
            str(self.counts.verified),
            str(self.counts.rejected),
        )
        return Group(Align(self._title, align="center"), display)


### question_counts.py ends here